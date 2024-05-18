# -*- coding: utf-8 -*-
"""Logging utils."""
import argparse
import logging
import time

from typing import Any, Dict, Union
from functools import wraps

import pandas


def show_time(logger: logging.Logger, total_time: Union[float, int]) -> None:
    """"""
    logger.info(f"\nFinished pipeline run after {total_time // 60:.0f} min {total_time % 60:.4f} secs.\n\n")

# FIXME: move to time.py
def timing(step):
    """Decorator to estimate execution time."""

    @wraps(step)
    def execute_step(
        artifacts: Dict[str, Any],
        args: argparse.Namespace = argparse.Namespace(),
        logger: logging.Logger = get_logger(),
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        start_time = time.perf_counter()

        step(
            artifacts=artifacts,
            args=args,
            logger=logger,
        )

        end_time = time.perf_counter() - start_time

        show_time(logger=logger, total_time=end_time)

        return step

    return execute_step

class Color:
    """A class for terminal color codes."""

    BOLD = "\033[1m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREY = "\033[90m"
    BLACK = "\033[30m"
    BOLD_WHITE = BOLD + WHITE
    BOLD_BLUE = BOLD + BLUE
    BOLD_GREEN = BOLD + GREEN
    BOLD_YELLOW = BOLD + YELLOW
    BOLD_RED = BOLD + RED
    BOLD_BLACK = BOLD + BLACK
    BOLD_GREY = BOLD + GREY
    END = "\033[0m"


class ColorLogFormatter(logging.Formatter):
    """A class for formatting colored logs."""

    FORMAT = "%(prefix)s%(msg)s%(suffix)s"

    LOG_LEVEL_COLOR = {
        "DEBUG": {"prefix": "", "suffix": ""},
        "INFO": {"prefix": Color.BLACK, "suffix": Color.END},
        "WARNING": {"prefix": Color.BOLD_YELLOW, "suffix": Color.END},
        "ERROR": {"prefix": Color.BOLD_RED, "suffix": Color.END},
        "CRITICAL": {"prefix": Color.BOLD_RED, "suffix": Color.END},
    }

    def format(self, record):
        """Format log records with a default prefix and suffix to terminal color codes that corresponds to the log
        level name.
        """
        if not hasattr(record, "prefix"):
            record.prefix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get(
                "prefix"
            )

        if not hasattr(record, "suffix"):
            record.suffix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get(
                "suffix"
            )

        formatter = logging.Formatter(self.FORMAT)
        return formatter.format(record)


def get_logger(name: str = "main", level: int = logging.INFO) -> logging.Logger:
    """Get the main logger.

    Args:
        name (str, optional): The logger name. Defaults to "main".
        level (int, optional): The logger level. Defaults to logging.INFO.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level=level)

    logger.propagate = False

    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(ColorLogFormatter())
        logger.addHandler(stream_handler)

    return logger


def log_tittle(msg: str, logger: logging.Logger = None) -> None:
    """Print the title message for an experiment.

    Args:
        msg (str): The message to print.
        logger (logging.Logger, optional): The logger to use. Defaults to None, so it creates a new one.
    """
    if logger is None:
        logger = get_logger()

    logger.info(f"\n\n{f' {msg} ':_^100}\n\n")


# FIXME: move to time.py
def time_pandas_udf_in_pipe(funct):
    """Decorator to estimate execution of pandas udf inside `.pipe()`"""

    @wraps(funct)
    def execute_udf(
        dataframe: pandas.DataFrame, logger: logging.Logger, comment: str = "", size: bool = True
    ) -> pandas.DataFrame:
        size_msg = ""
        if size:
            size_msg = f"with dimensions {dataframe.shape}"

        logger.info(f"-> Starting {comment} {size_msg}")
        start_time = time.perf_counter()

        output = funct(dataframe=dataframe, logger=logger, comment=comment, size=size)

        end_time = time.perf_counter() - start_time

        show_time(logger=logger, total_time=end_time)

        return output

    return execute_udf
