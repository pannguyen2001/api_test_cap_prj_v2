# import json
# import pandas as pd
# from typing import Dict
# from helpers import logger, time_execution_wrapper, print_test_result
# from case_setup import role_case_setup, account_case_setup, run_case
# from configs.constants import report_file_path, TEST_CASE_FILE_PATH, MODULETEST
# from common.common_setup import admin, teacher, student

# @time_execution_wrapper
# def main ():

#     # check env and package: cpu, storage, ...

#     # Define module test
#     module_test: str = MODULETEST.ACCOUNT.value

#     # create predata
#     # role_pre_data: Dict = role_case_setup()
#     account_pre_data: Dict = account_case_setup()

#     # test case setup
#     # run test case
#     df_run_case: pd.DataFrame = run_case(
#         file_path=TEST_CASE_FILE_PATH, file_type="excel", pre_data=account_pre_data
#     )
#     if df_run_case is None:
#         logger.warning("Execute test case failed.")
#         return
#     if df_run_case.empty:
#         logger.warning("No test case found.")
#         return

#     # Print result report
#     df_final_result: pd.DataFrame = df_run_case.copy()
#     print_test_result(df_run_case)

#     # save report to excel file
#     if not df_final_result[df_final_result["result"] == "Failed"].empty:
#         df_final_result["request_body"] = df_final_result["request_body"].map(lambda x: json.dumps(x) if x else x)
#         df_final_result["expected_result"] = df_final_result["expected_result"].map(lambda x: json.dumps(x) if x else x)
#         df_final_result[df_final_result["result"] == "Failed"].to_excel(
#             report_file_path, sheet_name=module_test, index=False
#         )
#         logger.success(f"Report saved to '{report_file_path}'.")

#     admin.client.logout()
#     student.client.logout()
#     teacher.client.logout()

# if __name__ == "__main__":
#     logger.info(f"{' Start testing ':=^50}\n")
#     main()
#     logger.success(f"{' End testing ':=^50}\n")
