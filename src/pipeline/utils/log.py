import logging


def get_logger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger("main")
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False

    return logger
