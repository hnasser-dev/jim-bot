import asyncio
from discord import Intents
from discord.ext import commands
from pathlib import Path
import os
from src.utils.globals import (
    BOT_TOKEN,
    BOT_TEST_TOKEN,
    DEBUG,
    DISCORD_ADMIN_ID,
    BOT_PREFIX,
    DB_PATH,
    COGS_PATH,
    TEST_COGS_PATH,
    ADMIN_COGS_PATH
)
from src.database.database_commands import DatabaseCommands
import sys


class MyBot(commands.Bot):
    def __init__(self, command_prefix, description, intents, admin_id, load_tests=False, load_admin_commands=False):
        super().__init__(
            command_prefix=command_prefix,
            description=description,
            intents=intents,
            case_insensitive=True,
            help_command=None
        )
        self.admin_id = admin_id
        self.load_tests = load_tests
        self.load_admin_commands = load_admin_commands
        self.database = DatabaseCommands(DB_PATH)

    async def on_ready(self):
        print(f"Logged in as {self.user}.")

    async def load_cogs(self):
        dirs_to_look = [COGS_PATH]
        if self.load_tests: dirs_to_look.append(TEST_COGS_PATH)
        if self.load_admin_commands: dirs_to_look.append(ADMIN_COGS_PATH)
        for dir_path in dirs_to_look:
            sys.path.insert(0, dir_path)
            for file in os.listdir(dir_path):
                if file.endswith(".py"):
                    extension_name = file[:-3]
                    try:
                        await self.load_extension(extension_name)
                    except commands.ExtensionError as e:
                        sys.exit(f"Error loading extension: {e}")
                    except Exception as f:
                        sys.exit(str(f))
                    else:
                        print(f"{self.description}: {extension_name} loaded")
            sys.path.pop(0)


async def main():
    token = BOT_TOKEN if DEBUG == "False" else BOT_TEST_TOKEN
    prefixes = [BOT_PREFIX, BOT_PREFIX.title()] # both lowercase and title case are options
    bot = MyBot(
        command_prefix=commands.when_mentioned_or(*prefixes),
        description="Jim Bot",
        intents=Intents.all(),
        admin_id=DISCORD_ADMIN_ID,
        load_admin_commands=True
    )
    await bot.start(token)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())