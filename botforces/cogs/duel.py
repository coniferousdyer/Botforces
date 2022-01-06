import discord
import asyncio
import random
from discord.ext import commands

from botforces.utils.api import get_users_last_submission
from botforces.utils.db import (
    get_duel_from_db,
    get_duels_from_db,
    get_problems_from_db,
    store_duel,
    remove_duel_from_db,
)
from botforces.utils.discord_common import create_duel_begin_embed, create_duels_embed
from botforces.utils.services import decide_verdict, separate_rating_and_tags


class Duel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def duel(self, ctx, usr: discord.User = None, *args):
        """
        Performs pre-duel actions, suggests a random problem to a user and begins the duel.
        """

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        # Checking if a user was mentioned
        if usr == None:
            await ctx.send(":x: Please mention whom you want to duel.")
            return

        if usr.bot or usr == self.client.user:
            await ctx.send(":x: You can't duel a bot.")
            return

        # Checking if the user mentioned themselves
        if usr == ctx.author:
            await ctx.send(":x: You can't duel yourself.")
            return

        reactMsg = await ctx.send(
            f"<@{usr.id}>, react to this message with :thumbsup: within 60 seconds to accept the duel."
        )

        # Waiting for the reaction
        try:
            await self.client.wait_for(
                "reaction_add",
                timeout=30.0,
                check=lambda reaction, user: user == usr
                and str(reaction.emoji) == "\N{THUMBS UP SIGN}"
                and reactMsg.id == reaction.message.id,
            )
        except asyncio.TimeoutError:
            await ctx.send(":x: Sorry, the duel expired because 30 seconds were up!")
            return
        else:
            await ctx.send(
                f"<@{usr.id}> has accepted the duel! Send handles of <@{ctx.message.author.id}> and <@{usr.id}> respectively like this within the next 60 seconds:\n```handles <handle of {ctx.author.display_name}> <handle of {usr.display_name}>```"
            )

            try:
                msg = await self.client.wait_for(
                    "message",
                    timeout=60.0,
                    check=lambda m: m.content.startswith("handles")
                    and m.channel == reactMsg.channel
                    and (m.author == usr or m.author == ctx.message.author)
                    and len(m.content.split()) == 3,
                )
            except asyncio.TimeoutError:
                await ctx.send(
                    ":x: Sorry, the duel expired because 60 seconds were up!"
                )
                return
            else:
                await ctx.send("Starting duel...")
                handles = msg.content.split()

            # Opening data.db and reading the problems into a list
            rating, tags = await separate_rating_and_tags(args)
            problemList = await get_problems_from_db(rating, tags)

            # In case no problems are found
            if len(problemList) == 0:
                await ctx.send(
                    ":x: Sorry, no problems could be found. Please try again."
                )
                return

            # Storing problem
            problem = problemList[random.randint(0, len(problemList) - 1)]
            Embed = await create_duel_begin_embed(problem, ctx.author, usr)
            await ctx.send(embed=Embed)
            await store_duel(problem, ctx.message.author, usr, handles)

    @commands.command()
    async def endduel(self, ctx):
        """
        Ends the duel and declares the winner.
        """

        # Searching duels in data.db to find the one which message author is part of
        duel = await get_duel_from_db(ctx.message.author)

        # If no duel with the user was found
        if duel == None:
            await ctx.send(":x: You are not taking part in a duel currently!")
            return

        async with ctx.typing():
            # Obtaining and comparing the last submissions of the two users
            user_submission, opponent_submission = await get_users_last_submission(
                ctx, duel
            )
            user_solved, opponent_solved = await decide_verdict(
                duel, user_submission, opponent_submission
            )

        # If both users solved the problem
        if user_solved and opponent_solved:
            if (
                user_submission["creationTimeSeconds"]
                <= opponent_submission["creationTimeSeconds"]
            ):
                await ctx.send(f"<@{duel[0]}> has won the duel against <@{duel[1]}>!")
            else:
                await ctx.send(f"<@{duel[1]}> has won the duel against <@{duel[0]}>!")

        # If only user_1 solved the problem
        elif user_solved:
            await ctx.send(f"<@{duel[0]}> has won the duel against <@{duel[1]}>!")

        # If only user_2 solved the problem
        elif opponent_solved:
            await ctx.send(f"<@{duel[1]}> has won the duel against <@{duel[0]}>!")

        # If neither solved the problem
        else:
            opponentID = None
            if ctx.message.author.id == duel[0]:
                opponentID = duel[1]
            else:
                opponentID = duel[0]

            reactMsg = await ctx.send(
                f"<@{opponentID}>, react to this message with :thumbsup: within 30 seconds to invalidate the duel."
            )

            # Waiting for the reaction
            try:
                await self.client.wait_for(
                    "reaction_add",
                    timeout=30.0,
                    check=lambda reaction, user: user.id == opponentID
                    and str(reaction.emoji) == "\N{THUMBS UP SIGN}"
                    and reactMsg.id == reaction.message.id,
                )
            except asyncio.TimeoutError:
                await ctx.send(
                    ":x: Sorry, the invalidation request expired because 30 seconds were up!"
                )
                return
            else:
                await ctx.send("Duel ended, neither won!")
                await remove_duel_from_db(duel)

    @commands.command()
    async def duelstats(self, ctx):
        """
        Displays information about ongoing duels.
        """

        duels = await get_duels_from_db()

        if len(duels) == 0:
            await ctx.send(":x: There are no ongoing duels!")
            return

        # Creating embed
        Embed = await create_duels_embed(duels)
        await ctx.send(embed=Embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Duel ready!")


def setup(client):
    client.add_cog(Duel(client))
