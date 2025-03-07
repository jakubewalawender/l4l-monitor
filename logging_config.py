import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging():
    """Sets up logging with rotating file handlers."""

    # Create 'logs' folder if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Create a logger for general info messages
    info_logger = logging.getLogger("luxuryforless_info")
    info_logger.setLevel(logging.INFO)

    # Create a rotating file handler for info messages (max size 1MB, 3 backups)
    info_handler = RotatingFileHandler("logs/luxuryforless_info.log", maxBytes=1_000_000, backupCount=3)
    info_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the info handler
    info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(info_formatter)

    # Add the handler to the info logger
    info_logger.addHandler(info_handler)

    # Create a logger for exception messages
    exception_logger = logging.getLogger("luxuryforless_exception")
    exception_logger.setLevel(logging.ERROR)

    # Create a rotating file handler for exceptions (max size 1MB, 3 backups)
    exception_handler = RotatingFileHandler("logs/luxuryforless_exception.log", maxBytes=1_000_000, backupCount=3)
    exception_handler.setLevel(logging.ERROR)

    # Create a formatter and add it to the exception handler
    exception_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    exception_handler.setFormatter(exception_formatter)

    # Add the handler to the exception logger
    exception_logger.addHandler(exception_handler)

    return info_logger, exception_logger
