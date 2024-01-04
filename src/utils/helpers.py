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
    timezone_code_url = 
    def __init__(self, code):
        self.code = code.upper()
        self.valid = self.check_valid_code()
        self.tz = pytz.timezone(self.code) if self.valid else None

    def check_valid_code(self):
        if self.code in pytz.all_timezones_set:
            return True
        return False


class DiscordCtx:
    def __init__(self, ctx: commands.Context, mentioned_user=None):
        self.ctx = ctx # for accessing attributes of the original ctx object
        self.user_id = str(ctx.author.id)
        self.user_name = str(ctx.author.name)
        self.server_id = str(ctx.guild.id) if ctx.guild else None
        self.server_name = str(ctx.guild)
        self.timestamp = self.get_timestamp_str(initial=True)
        self.mentioned_user = DiscordCtx.extract_id(mentioned_user) if mentioned_user else None

    async def reply_to_user(self, message: str, exec_outcome=ExecutionOutcome.DEFAULT, ping=False) -> None:
        """
        Replies to the user with an appropriate (emojified) message
        Logs activity via a custom logger
        """
        # prepend an appropriate emoji (if required) then reply to the user
        reply_msg = DiscordCtx.emojify_str(message, exec_outcome)
        await self.ctx.reply(reply_msg, mention_author=ping)

    def get_timestamp_str(self, initial=False, day_offset=0):
        date_format = "%Y-%m-%d %H:%M:%S"
        if initial: # if called from init
            return datetime.utcnow().strftime(date_format)
        timestamp = datetime.strptime(self.timestamp, date_format) + timedelta(day_offset)
        return timestamp.strftime(date_format)

    @staticmethod
    def emojify_str(msg, exec_outcome):
        """
        Given a specified exec_outcome, pre-pend an appropriate emoji (check mark or cross)
        to the specified msg
        """
        match exec_outcome.name:
            case "ERROR" | "WARNING":
                emoji_str = ":x: "
            case "DEFAULT":
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