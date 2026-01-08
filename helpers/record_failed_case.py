import json
import pandas as pd
from typing import Union
from configs.constants import datetime_today, today
from .logger import logger
from .logger_wrapper import logger_wrapper

@logger_wrapper
def record_fail_case(fail_case_data: Union[pd.DataFrame, pd.Series] = None) -> None:
    import os
    file_path: str = f"reports/{today}/fail_case_{datetime_today}.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
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