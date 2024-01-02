from discord import Intents
from discord.ext import commands
from pathlib import Path
import os
from utils.env import (
    BOT_TOKEN,
    BOT_TEST_TOKEN,
    DEBUG,
    DB_PATH
)
from database import DatabaseManager


class MyBot(commands.Bot):
    def __init__(self, command_prefix, description, intents):
        super().__init__(
            command_prefix=command_prefix,
            description=description,
            intents=intents
        )
        self.database = DatabaseManager(DB_PATH)

    async def on_ready(self):
        print(f"Logged in as {self.user}.")

    async def load_cogs(self):
        cogs_dir = f"{Path(__file__).parent}/cogs"
        print(cogs_dir)
        for file in os.listdir(cogs_dir):
            if file.endswith(".py"):
                extension_name = file[:-3]
                print(extension_name)
                try:
                    await self.load_extension(f"cogs.{extension_name}")
                except commands.ExtensionError as e:
                    print(e)
                else:
                    print(f"{extension_name} loaded")

    async def setup_hook(self):
        """ Runs when the bot first starts up """
        await self.database.connect()
        await self.load_cogs()


def main():
    token = BOT_TOKEN if DEBUG == "False" else BOT_TEST_TOKEN
    bot = MyBot(
        command_prefix="jim/",
        description="Jim Bot",
        intents=Intents.all()
    )
    bot.run(token)


if __name__ == "__main__":
    main()