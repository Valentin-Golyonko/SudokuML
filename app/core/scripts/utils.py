import logging
from functools import wraps
from time import perf_counter

logger = logging.getLogger(__name__)


def time_it(func):
    @wraps(func)
    def run_time(*args, **kwargs):
        t0 = perf_counter()
        result = func(*args, **kwargs)
        logger.debug(f"'{func.__name__}' = {(perf_counter() - t0):.6f}")
        return result

    return run_time


class Utils:
    pass
