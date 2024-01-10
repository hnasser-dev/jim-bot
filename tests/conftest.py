from main import MyBot
from discord import Intents
from src.cogs.commands import Commands
import pytest_asyncio
import discord.ext.test as dpytest
from src.utils.globals import BOT_PREFIX


@pytest_asyncio.fixture
async def bot():
    bot = MyBot(
        command_prefix=BOT_PREFIX,
        description="Test Bot",
        intents=Intents.all()
    )
    await bot._async_setup_hook() # setup the loop
    await bot.add_cog(Commands(bot))
    dpytest.configure(bot)
    yield bot
    # Teardown
    await dpytest.empty_queue() # empty the global message queue as test teardown