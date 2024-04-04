import logging
from time import time

logger = logging.getLogger(__name__)


def timer_func(func):
    def wrap_func(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        logger.debug(f"Function {func.__name__!r} executed in {(time() - start):.4f}s")
        return result

    return wrap_func


def a_timer_func(func):
    async def wrap_func(*args, **kwargs):
        start = time()
        result = await func(*args, **kwargs)
        logger.debug(f"Function {func.__name__!r} executed in {(time() - start):.4f}s")
        return result

    return wrap_func
