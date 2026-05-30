import json
import pandas as pd
from typing import Union
from configs.constants import error_report_file_path
from .logger import logger
from .logger_wrapper import logger_wrapper

@logger_wrapper
def record_fail_case(fail_case_data: Union[pd.DataFrame, pd.Series] = None) -> None:
    fail_case_data = fail_case_data[fail_case_data.notna()].to_dict()
    fail_case_data["request_body"] = json.dumps(fail_case_data["request_body"], indent=4)
    fail_case_data["detail"] = "\n".join(fail_case_data["detail"])

    with open(error_report_file_path, 'a') as file:
        for key, value in fail_case_data.items():
            file.write(f"{key}: {value}\n")
        file.write(f"\n{'':=^50}\n\n")
    logger.success(f"Record failed case to file: {error_report_file_path}")

