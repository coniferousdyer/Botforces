from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        The error handler.
        """
        
        message = ''

        if isinstance(error, commands.CommandNotFound):
            message = ":x: The command was not found! Type `-help` to check the list of available commands."
        elif isinstance(error, commands.MissingRequiredArgument):
            message = ":x: One or more arguments are missing!"
        elif isinstance(error, commands.TooManyArguments):
            message = ":x: Too many arguments were provided!"
        else:
            message = ":x: Something went wrong while running the command!"
            print(error)

        if message != '':
            await ctx.send(message)

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Error ready!")


def setup(client):
    client.add_cog(Error(client))
