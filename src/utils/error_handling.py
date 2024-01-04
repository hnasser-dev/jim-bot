from enum import Enum
from src.logs.logger_config import PROJECT_LOGGER


class ExecutionOutcome(Enum):
    ERROR = 2
    WARNING = 1
    DEFAULT = 0
    SUCCESS = -1


class ExecutionError:
    def __init__(self, contxt=None, level=ExecutionOutcome.DEFAULT, text="An unknown error has occurred.", exception=None):
        self.level = level
        self.text = text # readable text describing the issue
        self.exception = exception
        self.command_message = contxt.ctx.message if contxt else ""
        self.log_error() # when creating an object it should automatically log it

    def log_error(self):
        log_msg = f"{self.command_message}/{self.text}/{self.exception if self.exception else ''}"
        match self.level.name:
            case "ERROR":
                PROJECT_LOGGER.error(log_msg)
            case "WARNING":
                PROJECT_LOGGER.warning(log_msg)
            case _:
                PROJECT_LOGGER.debug(log_msg)

    @staticmethod
    def check_if_error(val):
        return isinstance(val, DatabaseError)


class DatabaseError(ExecutionError):
    pass


class ParseError(ExecutionError):
    pass