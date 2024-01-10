from discord.ext import commands
import pytest
import discord.ext.test as dpytest
from src.utils.globals import BOT_PREFIX


""" Two examples of how to use dpytest functions """
# @pytest.mark.asyncio
# async def test_ping(bot):
#     await dpytest.message(f"{BOT_PREFIX}ping")
#     assert dpytest.verify().message().content("Pong !")


# @pytest.mark.asyncio
# async def test_echo(bot):
#     await dpytest.message(f"{BOT_PREFIX}echo Hello world")
#     assert dpytest.verify().message().contains().content("Hello")