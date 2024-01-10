import asyncio
from discord import Intents
from discord.ext import commands
from pathlib import Path
import os
from src.utils.globals import (
    BOT_TOKEN,
    BOT_TEST_TOKEN,
    DEBUG,
    DB_PATH,
    COGS_PATH,
    TEST_COGS_PATH
)
from src.database.database_commands import DatabaseCommands
import sys


class MyBot(commands.Bot):
    def __init__(self, command_prefix, description, intents, load_tests=False):
        super().__init__(
            command_prefix=command_prefix,
            description=description,
            intents=intents,
            help_command=None
        )
        self.load_tests = load_tests
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

        if self.load_tests: # loading test cogs, for running tests
            for file in os.listdir(TEST_COGS_PATH):
                if file.endswith(".py"):
                    extension_name = file[:-3]
                    try:
                        await self.load_extension(f"tests.cogs.{extension_name}")
                    except commands.ExtensionError as e:
                        sys.exit(f"Error loading extension: {e}")
                    else:
                        print(f"{extension_name} loaded")


    async def setup_hook(self):
        """ Runs when the bot first starts up """
        await self.load_cogs()

    async def async_startup(self, bot_token):
        await self.start(bot_token)
        await self.setup_hook()  # Call setup after bot is connected

    async def async_shutdown(self):
        await self.close()


async def main():
    token = BOT_TOKEN if DEBUG == "False" else BOT_TEST_TOKEN
    bot = MyBot(
        command_prefix="jim/",
        description="Jim Bot",
        intents=Intents.all(),
    )
    await bot.start(token)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())