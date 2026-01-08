import pytest
import traceback
from typing import Callable
from functools import wraps
from string import Template
from .logger import logger

error_template = Template("""[${funct_name}] has error:
${error}""")

def logger_wrapper(func: Callable) -> Callable:
    # @logger.catch
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = "".join(traceback.TracebackException.from_exception(e).format())
            logger.error(error_template.safe_substitute(funct_name=func.__name__, error=tb))
            pytest.exit("End testing with error.")

    return wrap