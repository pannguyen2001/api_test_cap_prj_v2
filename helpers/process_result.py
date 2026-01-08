import json
import pandas as pd
from helpers import logger
from helpers import print_test_result
from configs.constants import report_file_path


def process_result(df_run_case: pd.DataFrame = None, module_test: str = "Unknown") -> None:
    if df_run_case is None:
        logger.warning("Execute test case failed.")
        return
    if df_run_case.empty:
        logger.warning("No test case found.")
        return

    # Print result report
    df_final_result: pd.DataFrame = df_run_case.copy()
    print_test_result(df_run_case)

    # save report to excel file
    if not df_final_result[df_final_result["result"] == "Failed"].empty:
        df_final_result["request_body"] = df_final_result["request_body"].map(lambda x: json.dumps(x) if x else x)
        df_final_result["expected_result"] = df_final_result["expected_result"].map(lambda x: json.dumps(x) if x else x)
        df_final_result[df_final_result["result"] == "Failed"].to_excel(
            report_file_path, sheet_name=module_test, index=False
        )
        logger.success(f"Report saved to '{report_file_path}'.")