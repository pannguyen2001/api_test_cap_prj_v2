import datetime
import json
import re
from typing import Dict
from .logger import logger
from .logger_wrapper import logger_wrapper
from .random_string import random_string

@logger_wrapper
def replace_random_string(data: str = "") -> str:
    if "random_string" in data:
        matches = re.findall(r"\{random_string\((.*?)\)\}", data)
        if not matches:
            logger.warning(f"Not found match random string format in '{data}'.")
            return data

        str_len = int(matches[0])
        random_str = random_string(str_len)
        replace_str = "{" + "random_string({})".format(str_len) + "}"
        data = data.replace(replace_str, random_str)
    return data

@logger_wrapper
def replace_datetime_format(data: str = "") -> str:
    # {datetime(%Y-%m-%d %H:%M:%S,0)} -> ["%Y-%m-%d %H:%M:%S", "7"] -> 2025-12-25 07:00:00 (local datetime)
    if "datetime" in data:
        matches = re.findall(r"\{datetime\((.*?)\)\}", data)
        if not matches:
            logger.warning(f"Not found match datetime format in '{data}'.")
            return data

        datetime_format, time_delta = matches[0].split(",")
        time_delta = float(time_delta)
        datetime_str: str = (datetime.datetime.now() + datetime.timedelta(hours=time_delta)).astimezone().strftime(datetime_format)
        data = data.replace(f"{{datetime({matches[0]})}}", datetime_str)
    return data

@logger_wrapper
def replace_data_by_setup_values(data: str = "", setup_data: Dict = None) -> Dict:
    if not data:
        raise Exception(f"[{replace_data_by_setup_values.__name__}] error: input data can not be None")
    if not setup_data:
        raise Exception(f"[{replace_data_by_setup_values.__name__}] error: input setup data can not be None")

    if not isinstance(data, str):
        data = json.dumps(data)

    for key, value in setup_data.items():
        if not isinstance(value, str):
            logger.warning(f"Value is not string. Convert to string type. Key: '{key}' - value: '{value}'. ")
            value = str(value)

        data = data.replace("{" + key + "}", value)
        data = data.replace('"{[' + key + ']}"', value)
        data = replace_random_string(data)
        data = replace_datetime_format(data)

    data = json.loads(data)
    return data



