import json
import pytest
from typing import List, Dict
from helpers import logger, logger_wrapper, replace_data_by_setup_values
from configs.constants import ROLE
from common.common_setup import role_predata_info

@pytest.fixture(scope="session")
@logger_wrapper
def role_case_setup(admin, student, teacher) -> Dict:
    predata_request_body_template: Dict = role_predata_info["predata"]
    need_clear_data_info: List = role_predata_info["need_clear"]
    pre_data: Dict = {}
    pre_data["admin_role_name"] = ROLE.ADMIN.value
    pre_data["student_role_name"] = ROLE.STUDENT.value
    pre_data["teacher_role_name"] = ROLE.STUDENT.value

    # clear data created by previous run.
    admin.RoleProcessResponse.clear_data(need_clear_data_info)

    # get all roles
    all_roles: List = admin.RoleProcessResponse.get_all_roles()
    if all_roles:
        for role in all_roles:
            if role.get("name") == pre_data["admin_role_name"]:
                pre_data["admin_role_id"] = role.get("_id")
            elif role.get("name") == pre_data["student_role_name"]:
                pre_data["student_role_id"] = role.get("_id")
            elif role.get("name") == pre_data["teacher_role_name"]:
                pre_data["teacher_role_id"] = role.get("_id")

    # # get role by id
    # admin_info: Dict = admin.RoleProcessResponse.get_role_by_id(pre_data["admin_role_id"])

    # create role
    role_01_request_body: Dict = predata_request_body_template["role_01"]
    role_01_request_body = replace_data_by_setup_values(role_01_request_body, pre_data)
    role_01_info: Dict = admin.RoleProcessResponse.create_new_role_with_check(role_01_request_body)
    pre_data["role_01_id"] = role_01_info.get("_id")
    pre_data["role_01_name"] = role_01_info.get("name")


    logger.info(json.dumps(pre_data, indent=4))
    return pre_data

