import json
import pytest
import pandas as pd
from typing import Dict
from configs.constants import FILE_TYPE, FILETYPE
from helpers import logger, time_execution_wrapper, print_test_result
from common.common_setup import admin, student, teacher
from common.client import Client
from .run_case import run_case
from configs.constants import report_file_path

# try pytest
class BaseTest:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = Client()
        self.__result = None
        self.__module_test = ""

    def setup_test(self, module_test: str = ""):
        self.__module_test = module_test

    @time_execution_wrapper
    def run_test(
        self,
        test_case_file_path: str = "",
        test_case_file_type: str = FILETYPE.EXCEL.name.lower(),
        pre_data: Dict = None,
        ):
        self.__result =  run_case(test_case_file_path, test_case_file_type, pre_data)
        return self.__result


    def tear_down(self):
        logger.success("All cases complete.")
        df_run_case: pd.DataFrame = self.__result
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
                report_file_path,
                sheet_name=self.__module_test,
                index=False
            )
            logger.success(f"Report saved to '{report_file_path}'.")

        admin.client.logout()
        student.client.logout()
        teacher.client.logout()