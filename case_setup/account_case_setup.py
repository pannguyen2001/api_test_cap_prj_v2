import json
import pytest
from typing import List, Dict
from .base_test import BaseTest
from helpers import logger, logger_wrapper, replace_data_by_setup_values
from common.common_setup import admin, account_predata_info, ROLE
from configs.constants import FILETYPE, TEST_CASE_FILE_PATH


@pytest.fixture
@logger_wrapper
def account_case_setup() -> Dict:
    predata_request_body_template: Dict = account_predata_info["predata"]
    need_clear_data_info: List = account_predata_info["need_clear"]
    pre_data: Dict = {}
    pre_data["admin_role_name"] = ROLE.ADMIN.value
    pre_data["student_role_name"] = ROLE.STUDENT.value
    pre_data["teacher_role_name"] = ROLE.STUDENT.value

    # clear data created by previous run.
    admin.AccountResponse.clear_data(need_clear_data_info)

    # get Role id, just for test integration
    all_roles: List = admin.RoleProcessResponse.get_all_roles()
    if all_roles:
        for role in all_roles:
            if role.get("name") == pre_data["admin_role_name"]:
                pre_data["admin_role_id"] = role.get("_id")
            elif role.get("name") == pre_data["student_role_name"]:
                pre_data["student_role_id"] = role.get("_id")
            elif role.get("name") == pre_data["teacher_role_name"]:
                pre_data["teacher_role_id"] = role.get("_id")

    # get all accounts
    all_accounts: List = admin.AccountResponse.get_all_accounts()
    if all_accounts:
        for account in all_accounts:
            if account.get("role_name") == pre_data["admin_role_name"]:
                pre_data["admin_account_id"] = account.get("_id")
            elif account.get("role_name") == pre_data["student_role_name"]:
                pre_data["student_account_id"] = account.get("_id")
            elif account.get("role_name") == pre_data["teacher_role_name"]:
                pre_data["teacher_account_id"] = account.get("_id")

    # # get account by id
    # admin_account_info: Dict = admin.AccountResponse.get_account_by_id(pre_data["admin_account_id"])

    # create role
    # Note that admin can not delete admin.
    # Therefore, if create admin account, can not use this to delete,
    # need go to db or use postman to manual delete.
    account_01_request_body: Dict = predata_request_body_template["account_01"]
    account_01_request_body = replace_data_by_setup_values(account_01_request_body, pre_data)
    account_01_info: Dict = admin.AccountResponse.create_new_account_with_check(account_01_request_body)
    if account_01_info:
        pre_data["account_01_id"] = account_01_info.get("_id")
        pre_data["account_01_name"] = account_01_info.get("full_name")

    logger.info(json.dumps(pre_data, indent=4))
    return pre_data
