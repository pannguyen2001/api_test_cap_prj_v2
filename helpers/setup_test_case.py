import json
import pandas as pd
from typing import Dict, Any, Optional
from helpers import logger, logger_wrapper, replace_string_by_dict_value, replace_data_by_setup_values

@logger_wrapper
def setup_test_case(
    test_case_info: Any = None,
    pre_data: Dict = None
    ) -> Optional[pd.DataFrame]:
    if test_case_info is None or len(test_case_info) == 0:
        logger.warning("No test case found.")
        return

    df_test_case: pd.DataFrame = pd.DataFrame(test_case_info)
    df_neccessary_case: pd.DataFrame = df_test_case[df_test_case["status"] == "Done"]
    skip_cases: pd.DataFrame = df_test_case[df_test_case["status"] != "Done"]
    logger.warning(f"Skip cases: {json.dumps(skip_cases['case_no'].tolist(), indent=4)}")
    if df_neccessary_case.empty:
        logger.warning("No necessary test case found.")
        return

    if not pre_data:
        logger.warning("No pre-data found.")
        return

    df_neccessary_case["api"] = df_neccessary_case["api"].map(lambda x: replace_string_by_dict_value(x, pre_data) if pd.notna(x) else x)

    df_neccessary_case["request_body"] = df_neccessary_case["request_body"].map(lambda x: replace_data_by_setup_values(x, pre_data) if pd.notna(x) else None)

    df_neccessary_case["expected_result"] = df_neccessary_case["expected_result"].map(lambda x: replace_data_by_setup_values(x, pre_data) if pd.notna(x) else None)

    df_neccessary_case["actual_result"] = ""

    logger.success("Test case setup successfully.")
    logger.info(f"Test case info:\n{json.dumps(df_neccessary_case.to_dict(orient='records'), indent=4)}")
    return df_neccessary_case