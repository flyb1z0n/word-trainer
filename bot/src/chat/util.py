from functools import wraps
import logging
import time
logger = logging.getLogger(__name__)

logger.setLevel("DEBUG")


def timed(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time_ns()/1000000
        result = func(*args, **kwargs)
        end = time.time_ns()/1000000
        logger.debug("{} ran in {}ms".format(func.__name__, round(end - start, 2)))
        return result

    return wrapper
