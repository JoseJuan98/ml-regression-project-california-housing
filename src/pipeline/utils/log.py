import logging


def get_logger():
    global logger
    logger: logging.Logger = logging.getLogger('main')
    logger.addHandler(logging.StreamHandler())


# Utils
get_logger()
