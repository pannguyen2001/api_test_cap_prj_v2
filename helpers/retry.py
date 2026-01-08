import time
from functools import wraps
from .logger import logger
from .logger_wrapper import logger_wrapper

def retry(
    times: int = 1,
    delay: int = 5,
    exceptions=(Exception,)
    ):
    def decorator(function):
        @logger_wrapper
        @wraps(function)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return function(*args, **kwargs)
                except exceptions as err:
                    logger.warning(
                        f"[{function.__name__}] "
                        f"Attempt {attempt}/{times} failed: {err}"
                    )
                    if attempt < times:
                        time.sleep(delay)
            raise Exception(f"[{function.__name__}] Failed after {times} attempts.")
        return wrapper
    return decorator
