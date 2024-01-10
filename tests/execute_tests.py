# modify where the script looks for modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import MyBot
from src.utils.globals import (
    BOT_TEST_TOKEN,
    BOT_TEST2_TOKEN,
    DISCORD_ADMIN_ID
)
import discord
from discord.ext import commands
import threading
import asyncio
import tests.response_bot as response_bot


async def start_tests(token, invoke_prefix, discord_admin_id):
    bot = commands.Bot(
        command_prefix="invoke_bot/",
        description="Invoke Bot",
        intents=discord.Intents.all(),
    )

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.description}.")

    @bot.command()
    async def commence_test(ctx):
        print("Commencing tests...")
        commands = ["sayhello", "saygoodbye bot1", "saygoodbye bot2"]
        for command in commands:
            await ctx.send(f"{invoke_prefix}{command}")
            await asyncio.sleep(1)

    await bot.start(token)


if __name__ == '__main__':
    # bot which runs in the background and responds to commands
    test_bot_prefix = "test_bot/"
    test_bot = threading.Thread(target=response_bot.run_bot, args=(MyBot, test_bot_prefix, DISCORD_ADMIN_ID, BOT_TEST_TOKEN))
    test_bot.start()

    # bot that runs test cases by invoking commands
    asyncio.run(start_tests(BOT_TEST2_TOKEN, invoke_prefix=test_bot_prefix, discord_admin_id=DISCORD_ADMIN_ID))

    test_bot.join()