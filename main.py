from discord import Intents
from discord.ext import commands
from pathlib import Path
import os
from src.utils.globals import (
    BOT_TOKEN,
    BOT_TEST_TOKEN,
    DEBUG,
    DB_PATH,
    COGS_PATH
)
from src.database.database_commands import DatabaseCommands
import sys


class MyBot(commands.Bot):
    def __init__(self, command_prefix, description, intents):
        super().__init__(
            command_prefix=command_prefix,
            description=description,
            intents=intents,
            help_command=None
        )
        self.database = DatabaseCommands(DB_PATH)

    async def on_ready(self):
        print(f"Logged in as {self.user}.")

    async def load_cogs(self):
        for file in os.listdir(COGS_PATH):
            if file.endswith(".py"):
                extension_name = file[:-3]
                try:
                    await self.load_extension(f"src.cogs.{extension_name}")
                except commands.ExtensionError as e:
                    sys.exit(f"Error loading extension: {e}")
                else:
                    print(f"{extension_name} loaded")

    async def setup_hook(self):
        """ Runs when the bot first starts up """
        await self.load_cogs()


def main():
    token = BOT_TOKEN if DEBUG == "False" else BOT_TEST_TOKEN
    bot = MyBot(
        command_prefix="jim/",
        description="Jim Bot",
        intents=Intents.all(),
    )
    bot.run(token)


if __name__ == "__main__":
    main()