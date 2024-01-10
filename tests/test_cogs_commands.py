from discord.ext import commands
import pytest
import discord.ext.test as dpytest
import textwrap


@pytest.mark.asyncio
async def test_help(bot):
    await dpytest.message("jim/help")
    expected_response = textwrap.dedent("""\
        `jim/register` --> register yourself for tracking
        `jim/deregister` --> deregister yourself from tracking
        `jim/registerserver` --> register this server for tracking
        `jim/joinserver` --> associate yourself with this server
        `jim/leaveserver` --> disassociate yourself from this server
        `jim/sesh [day_offset]` --> record a gym session (`day_offset` can record seshes `up to 7 days into the past`)
        `jim/seshterday` --> record a gym session for yesterday (`day offset = -1`)
        `jim/visits [@user]` --> see how many times you (or someone else) has been to the gym
        `jim/last <N> [@user]` --> look at your (or someone else's) `last N gym visits`
        `jim/lastvisit [@user]` --> look up when you (or someone else) last went to the gym
        `jim/table` --> show details for users registered in this server
        `jim/all` --> same as `jim/table`
        `jim/timezone` --> retrieve your current timezone (default UTC)
        `jim/settimezone <timezone>` --> set yourself a new timezone (`jim/settimezone details` for more details)
        `jim/graph [@user]` --> view your (or someone else's) gym visits as a graph
        `jim/updatename` --> update your name in the database to your current Discord username
        `jim/help` --> *commandception intensifies*
    """)
    assert dpytest.verify().message().content(expected_response)


# @pytest.mark.asyncio
# async def test_ping(bot):
#     await dpytest.message(f"jim/ping")
#     assert dpytest.verify().message().content("Pong !")


# @pytest.mark.asyncio
# async def test_echo(bot):
#     await dpytest.message(f"jim/echo Hello world")
#     assert dpytest.verify().message().contains().content("Hello")