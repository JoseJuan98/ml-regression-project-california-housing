import logging

from src.microservice.api.endpoint import app


def get_logger(level: int = logging.INFO) -> logging.Logger:
    """
    Method to get the logger of the flask application

    :param level: level which will show the logs
    :return:
    :rtype: logging.Logger
    """
    # remove default handler set by Flask to add new format
    for hdl in app.logger.handlers[:]:
        if isinstance(hdl, logging.StreamHandler):
            app.logger.removeHandler(hdl)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    app.logger.addHandler(handler)

    app.logger.setLevel(level)
    app.logger.propagate = False

    return app.logger
