import logging
from logging.handlers import RotatingFileHandler
import os


def configure_logging(app):
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

def setup_logging(log_file='app.log', level=logging.DEBUG, max_bytes=1000000, backup_count=3):
    """
    Sets up logging configuration.

    :param log_file: The file where logs will be saved.
    :param level: The logging level.
    :param max_bytes: Maximum file size before rotating logs.
    :param backup_count: Number of backup files to keep.
    """
    # Ensure the log directory exists
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a rotating file handler
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setLevel(level)
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Get the root logger and configure it
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
