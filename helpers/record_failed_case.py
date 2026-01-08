import datetime
import json
import os
import pandas as pd
from typing import Union
from configs.constants import today, DATETIMEFORMAT, VN_TIME_ZONE
from .logger import logger
from .logger_wrapper import logger_wrapper

@logger_wrapper
def record_fail_case(fail_case_data: Union[pd.DataFrame, pd.Series] = None) -> None:
    current_datetime: str = datetime.datetime.now().astimezone(VN_TIME_ZONE).strftime(DATETIMEFORMAT.DATETIME_V2.value)
    file_path: str = f"./reports/{today}/fail_case_{current_datetime}.txt"
    directory = os.path.dirname(file_path)
    # Create all necessary parent directories if they don't exist
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"Directories created: {directory}")

    fail_case_data = fail_case_data[
        [
            "case_no",
            "priority",
            "case_type",
            "role",
            "description",
            "expected_result",
            "detail",
            "datetime",
            "method",
            "api",
            "request_body"
        ]
    ]
    fail_case_data = fail_case_data[fail_case_data.notna()].to_dict()
    fail_case_data["request_body"] = json.dumps(fail_case_data["request_body"], indent=4)
    fail_case_data["detail"] = "\n".join(fail_case_data["detail"])

    with open(file_path, 'a') as file:
        for key, value in fail_case_data.items():
            file.write(f"{key} : {value}\n")
        file.write(f"\n{'':=^50}\n\n")
    logger.success(f"Record failed case to file: {file_path}")