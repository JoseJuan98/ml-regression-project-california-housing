# -*- coding: utf-8 -*-
"""Logging utils."""
import argparse
import logging
import time

from typing import Any, Dict, Union
from functools import wraps

import pandas


def get_logger(level: int = logging.INFO) -> logging.Logger:
    """Get main logger used by the project."""
    logger = logging.getLogger("main")
    logger.setLevel(level=level)

    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
    logger.propagate = False

    return logger


def show_time(logger: logging.Logger, total_time: Union[float, int]) -> None:
    """"""
    logger.info(f"\nFinished pipeline run after {total_time // 60:.0f} min {total_time % 60:.4f} secs.\n\n")


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
