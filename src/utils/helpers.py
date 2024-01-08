from discord.ext import commands
from datetime import datetime, timedelta
import pytz
from enum import Enum
from src.utils.error_handling import ExecutionOutcome


class DayOffset(Enum):
    TODAY = 0
    YESTERDAY = -1
    TWO_DAYS_AGO = -2
    THREE_DAYS_AGO = -3
    FOUR_DAYS_AGO = -4
    FIVE_DAYS_AGO = -5
    SIX_DAYS_AGO = -6
    SEVEN_DAYS_AGO = -7


class DBTimezone:
    def __init__(self, identifier):
        self.identifier = "UTC" if identifier.lower() == "utc" else identifier.title()
        self.pytz_tz = self.get_pytz_tz()

    def get_pytz_tz(self):
        if self.identifier in pytz.all_timezones_set:
            return pytz.timezone(self.identifier)

    def get_local_time_now(self):
        self.local_tz = pytz.timezone(self.identifier)

    @staticmethod
    def get_local_time(time_unix, pytz_tz):
        dt_utc = datetime.fromtimestamp(time_unix)
        return pytz.utc.localize(dt_utc).astimezone(pytz_tz).replace(tzinfo=None)

    @staticmethod
    def days_ago_str(curr_unix: float, past_unix: float):
        days_ago = int((curr_unix - past_unix) / 86400)
        match days_ago:
            case 0:
                return "<1 day ago"
            case 1:
                return "1 day ago"
            case _ if days_ago > 1:
                return f"{days_ago} days ago"
            
class DiscordCtx:
    def __init__(self, ctx: commands.Context, mentioned_user=None):
        self.ctx = ctx # for accessing attributes of the original ctx object
        self.user_id = str(ctx.author.id)
        self.user_name = str(ctx.author.name)
        self.server_id = str(ctx.guild.id) if ctx.guild else None
        self.server_name = str(ctx.guild)
        self.timestamp = self.get_unix_timestamp_int(initial=True)
        self.mentioned_user = DiscordCtx.extract_id(mentioned_user) if mentioned_user else None

    async def reply_to_user(self, message: str, exec_outcome=ExecutionOutcome.DEFAULT, ping=False) -> None:
        """
        Replies to the user with an appropriate (emojified) message
        Logs activity via a custom logger
        """
        # prepend an appropriate emoji (if required) then reply to the user
        reply_msg = DiscordCtx.emojify_str(message, exec_outcome)
        await self.ctx.reply(reply_msg, mention_author=ping)
    
    def get_unix_timestamp_int(self, initial=False, day_offset=0):
        if initial:
            return datetime.utcnow().timestamp()
        return self.timestamp + (day_offset * 86400)


    @staticmethod
    def emojify_str(msg, exec_outcome):
        """
        Given a specified exec_outcome, pre-pend an appropriate emoji (check mark or cross)
        to the specified msg
        """
        match exec_outcome.name:
            case "ERROR" | "WARNING":
                emoji_str = ":x: "
            case "SUCCESS":
                emoji_str = ":white_check_mark: "
            case _:
                emoji_str = ""
        return emoji_str + msg
    
    @staticmethod
    def extract_id(ping_text:str) -> str:
        """
        Convert <@id> to <id>, as a string.
        """
        return ping_text.replace('<', '').replace('>', '').replace('@', '')