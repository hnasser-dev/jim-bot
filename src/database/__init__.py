import sqlite3
from utils.helpers import ExecutionOutcome, DiscordCtx
from utils.globals import LOG_FILE_PATH


""" Logging Configuration """
from logs.log_handler import MyLogger
from pathlib import Path
file_stem = Path(__file__).stem # get name of the current file (without .py)
src_dir = Path(__file__).parent
MY_LOGGER = MyLogger(
    file_name=file_stem,
    log_file_path=LOG_FILE_PATH
)


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            # self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print("Database connected.")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("Database disconnected.")

    def execute_query(self, query, params={}) -> list:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()


class DatabaseError:
    def __init__(self, contxt:DiscordCtx, level=ExecutionOutcome.DEFAULT, text="An unknown error has occurred.", exception=None):
        self.level = level
        self.text = text # readable text describing the issue
        self.exception = exception
        self.command_message = contxt.ctx.message
        self.log_error() # when creating an object it should automatically log it

    def log_error(self):
        log_msg = f"{self.command_message}/{self.text}/{self.exception if self.exception else ''}"
        match self.level.name:
            case "ERROR":
                MY_LOGGER.logger.error(log_msg)
            case "WARNING":
                MY_LOGGER.logger.warning(log_msg)
            case _:
                MY_LOGGER.logger.debug(log_msg)

    @staticmethod
    def check_if_error(val):
        return isinstance(val, DatabaseError)


# class CustomRowFactory:
#     def __init__(self, cursor, row):
#         for idx, col in enumerate(cursor.description):
#             setattr(self, col[0], row[idx])

        
# def dict_factory(cursor, row):
#     """
#     Allows sqlite3 row data to be returned as a dictionary (per row)
#     (By default in sqlite3, rows are returned as tuples)
#     Usage:
#         conn.row_factory = dict_factory
#     """
#     fields = [column[0] for column in cursor.description]
#     return {key:value for key,value in zip(fields, row)}