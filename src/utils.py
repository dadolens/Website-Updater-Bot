import logging
import logging.handlers
import sys


def setup_logging(log_file: str) -> logging.Logger:
    logger = logging.getLogger('bot')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=7)
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(formatter)

    logger.addHandler(log_handler)
    return logger


def flush():
    sys.stdout.flush()
    sys.stderr.flush()
