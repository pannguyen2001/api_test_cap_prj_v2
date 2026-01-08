import json
import datetime
import pandas as pd
import pytest
from typing import Dict, List, Union
from string import Template
from requests import Response
from helpers.setup_test_case import setup_test_case
from helpers.time_execution_wrapper import time_execution_wrapper
from helpers.record_failed_case import record_fail_case
from configs.constants import ROLE, APIMETHOD, VN_TIME_ZONE, DATETIMEFORMAT
from .logger import logger
from .logger_wrapper import logger_wrapper


error_message: Dict = {
    "key_not_in_list": Template("[FAILED] Key: '${expected}' is not in list of keys: ${actual}."),
    "value_not_in_list": Template("[FAILED] Value: '${expected}' is not in list of values: ${actual}."),
    "status_code_not_equal": Template("[FAILED] Status code is not equal. Expected: ${expected}, Actual: ${actual}. Detail message: ${message}"),
    "value_not_equal": Template("[FAILED] Value is not equal. Expected: '${expected}', Actual: '${actual}'."),
    "no_data_found": Template("[FAILED] No data found."),
    "request_error": Template("[FAILED] Request error:\nStatus:${status}.\nText:${text}.")
}
passed_message: Dict = {
    "key_in_list": Template("[PASSED] Key: '${expected}' is in list of keys: ${actual}."),
    "value_in_list": Template("[PASSED] Value: '${expected}' is in list of values: '${actual}'."),
    "status_code_equal": Template("[PASSED] Status code is equal. Expected: ${expected}, Actual: ${actual}."),
    "value_equal": Template("[PASSED] Value is equal. Expected: '${expected}', Actual: '${actual}'."),
}

@logger_wrapper
def assert_error_response(
    row: Union[pd.DataFrame, pd.Series] = None,
    status_code: int = 200,
    res_message: str = ""
    ) -> bool:
    if status_code >= 400:
        request_error_message: str = error_message["request_error"].safe_substitute(status=status_code, text=res_message)
        logger.error(request_error_message)
        row["detail"].append(request_error_message)
        record_fail_case(row)
        pytest.fail(request_error_message)
        return False
    return True

@logger_wrapper
def assert_status_code(
    row: Union[pd.DataFrame, pd.Series] = None,
    status_code: int = 200,
    value: int = 200,
    res_message: str = ""
    ) -> bool:
    if status_code != value:
        status_code_not_equal_error_message: str = error_message["status_code_not_equal"].safe_substitute(expected=value, actual=status_code, message=res_message)
        logger.error(status_code_not_equal_error_message)
        row["detail"].append(status_code_not_equal_error_message)
        record_fail_case(row)
        pytest.fail(status_code_not_equal_error_message)
        return False
    logger.success(passed_message["status_code_equal"].safe_substitute(expected=value, actual=status_code))
    return True

@logger_wrapper
def assert_no_data_found(row: Union[pd.DataFrame, pd.Series] = None, data: any = None) -> bool:
    logger.error(error_message["No data found"])
    row["detail"].append(error_message["No data found"])
    record_fail_case(row)
    pytest.fail(error_message["No data found"])
    return False

@logger_wrapper
def assert_key_value(
    row: Union[pd.DataFrame, pd.Series] = None,
    data: Union[List, Dict] = None,
    key: str = ""
    ) -> bool:
    if isinstance(data, list):
        key_list: list = data[0].keys()
    elif isinstance(data, dict):
        key_list: list = data.keys()
    if key not in key_list:
        key_not_in_list_error_message: str = error_message["key_not_in_list"].safe_substitute(expected=key, actual=key_list)
        logger.error(key_not_in_list_error_message)
        row["detail"].append(key_not_in_list_error_message)
        record_fail_case(row)
        pytest.fail(key_not_in_list_error_message)
        return False
    else:
        logger.success(passed_message["key_in_list"].safe_substitute(expected=key, actual=key_list))
        return True

@logger_wrapper
def assert_data_value(
    row: Union[pd.DataFrame, pd.Series] = None,
    data: Union[List, Dict] = None,
    key: str = "",
    value: str = ""
):
    if isinstance(data, list):
        actual_detail: list = [i.get(key) for i in data]
        if value not in actual_detail:
            value_not_in_list_error_message: str = error_message["value_not_in_list"].safe_substitute(expected=value, actual=actual_detail)
            logger.error(value_not_in_list_error_message)
            row["detail"].append(value_not_in_list_error_message)
            record_fail_case(row)
            pytest.fail(value_not_in_list_error_message)
            return False
        else:
            logger.success(passed_message["value_in_list"].safe_substitute(expected=value, actual=actual_detail))
            return True

    if isinstance(data, dict):
        actual_result = data.get(key)
        if actual_result != value:
            value_not_equal_error_message: str = error_message["value_not_equal"].safe_substitute(expected=value, actual=actual_result)
            logger.error(value_not_equal_error_message)
            row["detail"].append(value_not_equal_error_message)
            record_fail_case(row)
            pytest.fail(value_not_equal_error_message)
            return False
        else:
            logger.success(passed_message["value_equal"].safe_substitute(expected=value, actual=actual_result))
            return True

@time_execution_wrapper
@logger_wrapper
def run_case(
    admin,
    student,
    teacher,
    test_case_info: Union[List, pd.DataFrame] = None,
    pre_data: Dict = None,
    module_test: str = "Unknown"
    ) -> None:
    if test_case_info is None or len(test_case_info) == 0:
        logger.error("Need test case to execute.")
        return
    if not isinstance(test_case_info, pd.DataFrame) or not isinstance(test_case_info, List):
        test_case_info = pd.DataFrame([test_case_info])

    df_test_case: Union[pd.DataFrame, None] = setup_test_case(test_case_info, pre_data)
    if df_test_case is None:
        logger.error("Setup test case failed.")
        return

    df_test_case["result"] = [None for i in range(df_test_case.shape[0])]
    df_test_case["detail"] = [list() for i in range(df_test_case.shape[0])]
    df_test_case["datetime"] = datetime.datetime.now().astimezone(VN_TIME_ZONE).strftime(DATETIMEFORMAT.DATETIME.value)

    for index, row in df_test_case.iterrows():
        logger.info(f"\n---------- Run case: {row['case_no']} - {row['description']} ----------")
        if row["role"] == ROLE.ADMIN.value:
            user = admin
        elif row["role"] == ROLE.STUDENT.value:
            user = student
        elif row["role"] == ROLE.TEACHER.value:
            user = teacher
        else:
            logger.error(f"Role: '{row['role']}' is not supported.")
            continue

        res: Response = None
        request_body: any = row["request_body"]
        logger.info(f"Request body:\n{json.dumps(request_body, indent=4)}")
        if row["method"] == APIMETHOD.GET.value:
            res = user.client.get(url=row["api"],json=row["request_body"])
        elif row["method"] == APIMETHOD.POST.value:
            res = user.client.post(url=row["api"],json=row["request_body"])
        elif row["method"] == APIMETHOD.PUT.value:
            res = user.client.put(url=row["api"],json=row["request_body"])
        elif row["method"] == APIMETHOD.PATCH.value:
            res = user.client.patch(url=row["api"],json=row["request_body"])
        elif row["method"] == APIMETHOD.DELETE.value:
            res = user.client.delete(url=row["api"],json=row["request_body"])

        logger.info(f"Response:\n{res.status_code}, {res.text}")
        status_code: int = res.status_code
        res_message: str = res.text if status_code >=400 else ""
        logger.info(f"Expected result: {row['expected_result']}")

        for key, value in row["expected_result"].items():
            logger.info(f"Key: {key}, Value: {value}")
            assert_error_response_result: bool = assert_error_response(row, status_code, res_message)
            if not assert_error_response_result:
                continue
            if key == "status_code":
                assert_status_code_result: bool = assert_status_code(row, status_code, value, res_message)
                if not assert_status_code_result:
                    continue
            else:
                data = res.json()
                if not data:
                    assert_no_data_found()
                    continue
                assert_key_value(row, data, key)
                assert_data_value(row, data, key, value)

        logger.success(f"\n---------- Done case: {row['case_no']} - {row['description'] } ----------")