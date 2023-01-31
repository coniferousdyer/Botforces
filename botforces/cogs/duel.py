"""
The Duel class, containing all the commands related to the dueling system.
"""


import logging
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
from botforces.utils.services import (
    decide_verdict,
    separate_rating_and_tags,
    verify_handles,
)
from botforces.utils.helpers import get_unsolved_problems


class Duel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def duel(self, ctx, opponent: discord.User = None, *args):
        """
        Performs pre-duel actions, suggests a random problem to a user and begins the duel.
        """

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        # Checking if a user was mentioned
        if opponent is None:
            await ctx.send(":x: Please mention whom you want to duel.")
            return

        if opponent.bot or opponent == self.client.user:
            await ctx.send(":x: You can't duel a bot.")
            return

        # Checking if the user mentioned themselves
        if opponent == ctx.author:
            await ctx.send(":x: You can't duel yourself.")
            return

        # Checking if the user is already in a duel
        if await get_duel_from_db(ctx.author) is not None:
            await ctx.send(":x: You are already in a duel!")
            return

        reactMsg = await ctx.send(
            f"<@{opponent.id}>, react to this message with :thumbsup: within 30 seconds to accept the duel."
        )

        # Waiting for the reaction
        try:
            await self.client.wait_for(
                "reaction_add",
                timeout=30.0,
                check=lambda reaction, user: user == opponent
                and str(reaction.emoji) == "\N{THUMBS UP SIGN}"
                and reactMsg.id == reaction.message.id,
            )
        except asyncio.TimeoutError:
            await ctx.send(":x: Sorry, the duel expired because 30 seconds were up!")
            return
        else:
            await ctx.send(
                f"<@{opponent.id}> has accepted the duel! Send handles of <@{ctx.message.author.id}> and <@{opponent.id}> respectively like this within the next 60 seconds:\n```handles <handle of {ctx.author.display_name}> <handle of {opponent.display_name}>```"
            )

            try:
                msg = await self.client.wait_for(
                    "message",
                    timeout=60.0,
                    check=lambda m: m.content.startswith("handles")
                    and m.channel == reactMsg.channel
                    and (m.author == opponent or m.author == ctx.message.author)
                    and len(m.content.split()) == 3,
                )
            except asyncio.TimeoutError:
                await ctx.send(
                    ":x: Sorry, the duel expired because 60 seconds were up!"
                )
                return
            else:
                handles = msg.content.split()
                verified = await verify_handles(ctx, handles[1], handles[2])
                if not verified:
                    await ctx.send(
                        ":x: Sorry, the duel expired because at least one of the handles is invalid!"
                    )
                    return

                await ctx.send("Starting duel...")

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
            problem = await get_unsolved_problems(
                ctx, [handles[1], handles[2]], problemList, handles_provided=True
            )

            # In case no unsolved problems are found
            if problem is None:
                await ctx.send(
                    ":x: Sorry, no unsolved problems could be found. Please try again."
                )
                return

            Embed = await create_duel_begin_embed(problem[0], ctx.author, opponent)
            await ctx.send(embed=Embed)
            await store_duel(
                problem[0], ctx.message.author, opponent, handles[1], handles[2]
            )

    @commands.command()
    async def endduel(self, ctx):
        """
        Ends the duel and declares the winner.
        """

        # Searching duels in data.db to find the one which message author is part of
        duel = await get_duel_from_db(ctx.message.author)

        # If no duel with the user was found
        if duel is None:
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
                await ctx.send(
                    f"<@{duel['user1_id']}> has won the duel against <@{duel['user2_id']}>!"
                )
            else:
                await ctx.send(
                    f"<@{duel['user2_id']}> has won the duel against <@{duel['user1_id']}>!"
                )

        # If only user_1 solved the problem
        elif user_solved:
            await ctx.send(
                f"<@{duel['user1_id']}> has won the duel against <@{duel['user2_id']}>!"
            )

        # If only user_2 solved the problem
        elif opponent_solved:
            await ctx.send(
                f"<@{duel['user2_id']}> has won the duel against <@{duel['user1_id']}>!"
            )

        # If neither solved the problem
        else:
            opponentID = None
            if ctx.message.author.id == duel["user1_id"]:
                opponentID = duel["user2_id"]
            else:
                opponentID = duel["user1_id"]

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
        logging.info("-Duel ready!")


def setup(client):
    client.add_cog(Duel(client))
