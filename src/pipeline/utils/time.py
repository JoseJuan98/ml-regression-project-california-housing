# -*- coding: utf-8 -*-
"""Time utils.

This module provides a time_it function that can be used to measure the time taken by a function to execute.
"""

import time

from functools import wraps

from .log import get_logger

logger = get_logger(__name__)


def time_it(name: str = ""):
    """Decorator to estimate execution time.

    Examples:
        >>> @time_it(name="Function")
        >>> def some_function():
        >>>     pass
    """

    def decorator(funct):
        @wraps(funct)
        def execute_funct(*args, **kwargs):
            start = time.perf_counter()

            output = funct(*args, **kwargs)

            end = time.perf_counter()

            total_time = end - start

            if total_time > 60:
                timed = f"{total_time / 60:.4f} mins"
            elif total_time > 1:
                timed = f"{total_time:.4f} secs"
            else:
                timed = f"{total_time * 1e3:.4f} ms"

            print(f"{f'{name} e' if name else 'E'}xecution time: {timed}.")

            return output, total_time

        return execute_funct

    return decorator
