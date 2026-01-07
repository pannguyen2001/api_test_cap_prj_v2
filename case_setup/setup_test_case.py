import json
import pandas as pd
from typing import Dict
from helpers import logger, logger_wrapper, load_data, replace_string_by_dict_value, replace_data_by_setup_values
from configs.constants import FILE_TYPE, FILETYPE, BASE_URL

@logger_wrapper
def setup_test_case(
    file_path: str = "",
    file_type: str = FILETYPE.EXCEL.name.lower(),
    pre_data: Dict = None
    ) -> None:
    test_case_info: Dict = load_data(file_path, file_type)

    df_test_case: pd.DataFrame = pd.DataFrame(test_case_info)
    df_neccessary_case: pd.DataFrame = df_test_case[df_test_case["status"] == "Done"]
    if df_neccessary_case.empty:
        logger.warning("No necessary test case found.")
        return

    if not pre_data:
        logger.warning("No pre-data found.")
        return

    # df_neccessary_case["api"] = BASE_URL + df_neccessary_case["api"]
    df_neccessary_case["api"] = df_neccessary_case["api"].map(lambda x: replace_string_by_dict_value(x, pre_data) if pd.notna(x) else x)

    df_neccessary_case["request_body"] = df_neccessary_case["request_body"].map(lambda x: replace_data_by_setup_values(x, pre_data) if pd.notna(x) else None)

    df_neccessary_case["expected_result"] = df_neccessary_case["expected_result"].map(lambda x: replace_data_by_setup_values(x, pre_data) if pd.notna(x) else None)

    logger.success("Test case setup successfully.")
    logger.info(f"Test case info:\n{json.dumps(df_neccessary_case.to_dict(orient='records'), indent=4)}")
    return df_neccessary_case