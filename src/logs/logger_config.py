import logging
from src.utils.globals import LOG_FILE_PATH


def setup_logger(name, log_file_path, logger_level=logging.DEBUG):
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(filename)s:%(name)s:%(message)s')
    # log to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # log to file
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    # logger
    logger = logging.getLogger(name)
    logger.setLevel(logger_level)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


"""
Usage: PROJECT_LOGGER.<level>/('<log_message>')
This logger will log everything (DEBUG and above) to both the console and to the log file.
"""
PROJECT_LOGGER = setup_logger("project_logger", LOG_FILE_PATH)