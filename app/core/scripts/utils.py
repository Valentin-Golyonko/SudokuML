import logging
from datetime import timedelta
from functools import wraps
from time import perf_counter

logger = logging.getLogger(__name__)


def atime_it(func):
    @wraps(func)
    async def run_time(*args, **kwargs):
        time_start = perf_counter()
        result = await func(*args, **kwargs)
        time_end = perf_counter()
        logger.debug(f"'{func.__name__}' = {timedelta(seconds=time_end - time_start)}")
        return result

    return run_time


def time_it(func):
    @wraps(func)
    def run_time(*args, **kwargs):
        time_start = perf_counter()
        result = func(*args, **kwargs)
        time_end = perf_counter()
        logger.debug(f"'{func.__name__}' = {timedelta(seconds=time_end - time_start)}")
        return result

    return run_time


class Utils:
    pass
