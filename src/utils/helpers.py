from discord.ext import commands
from datetime import datetime
import pytz
from enum import Enum
from utils.env import LOG_FILE_PATH


""" Logging Configuration """
from logs.log_handler import MyLogger
from pathlib import Path
file_stem = Path(__file__).stem # get name of the current file (without .py)
src_dir = Path(__file__).parent
MY_LOGGER = MyLogger(
    file_name=file_stem,
    log_file_path=LOG_FILE_PATH
)


class ExecutionOutcome(Enum):
    ERROR = 2
    WARNING = 1
    DEFAULT = 0
    SUCCESS = -1


class DiscordCtx:
    def __init__(self, ctx: commands.Context, *args):
        self.ctx = ctx # for accessing attributes of the original ctx object
        self.user_id = str(ctx.author.id)
        self.user_name = str(ctx.author.name)
        self.server_id = str(ctx.guild.id)
        self.server_name = str(ctx.guild)
        self.timestamp = str(curr_time_utc())

    async def report(self, bot_message: str, ping=False, log_message=None, exec_outcome=ExecutionOutcome.DEFAULT) -> None:
        """
        Replies to the user with an appropriate (emojified) message
        Logs activity via a custom logger
        """
        # prepend an appropriate emoji (if required) then reply to the user
        reply_msg = DiscordCtx.emojify_str(bot_message, exec_outcome)
        await self.reply_to_user(reply_msg, ping)

        """
        logging:
            - error: logger.error
            - unsuccessful action: logger.warning
            - successful action: logger.debug        
        """
        full_log_message = f"{log_message} ({self.ctx.message})" if log_message else f"{bot_message} ({self.ctx.message})"
        match exec_outcome.name:
            case "ERROR":
                MY_LOGGER.logger.error(full_log_message)
            case "WARNING":
                MY_LOGGER.logger.warning(full_log_message)
            case _:
                MY_LOGGER.logger.debug(full_log_message)

    async def reply_to_user(self, msg=None, ping=False):
        if ping:
            await self.ctx.reply(msg, mention_author=True)
        else:
            await self.ctx.reply(msg, mention_author=False)

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


""" Helper Functions - used for multiple commands """

def curr_time_utc() -> datetime:
    """
    Return current datetime for UTC.
    """
    return datetime.now(pytz.timezone('UTC'))


def curr_time_local(tz) -> datetime:
    """
    Return current datetime for for a given IANA timezone.
    """
    return datetime.now(pytz.timezone(tz))


def extract_id(ping_text:str) -> str:
    """
    Convert <@id> to <id>, as a string.
    """
    return ping_text.replace('<', '').replace('>', '').replace('@', '')
