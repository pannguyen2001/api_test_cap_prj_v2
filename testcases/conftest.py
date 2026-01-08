import json
import pytest
import os
from typing import Dict
from helpers import logger
from helpers import load_data
from common.user import User
from configs.constants import ROLE
from case_setup.account_case_setup import account_case_setup
from case_setup.role_case_setup import role_case_setup


logger.info(f"{' Load common info and setup ':=^50}")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger.info(f"Base dir: {base_dir}")

# ========== Load predata ===========
# Role
role_request_body_template_file_path: str = os.path.join(base_dir, "data", "request_body_template", "role_request_body_template.json")
role_predata_info: Dict = load_data(role_request_body_template_file_path, "json")
logger.success(f"Load role predata successfully:\n{json.dumps(role_predata_info, indent=4)}")

# Account
account_request_body_template_file_path: str = os.path.join(base_dir, "data", "request_body_template", "account_request_body_template.json")
account_predata_info: Dict = load_data(account_request_body_template_file_path, "json")
logger.success(f"Load account predata successfully:\n{json.dumps(account_predata_info, indent=4)}")


# =========== Load client info from USER_CONFIG_FILE_PATH ==========
user_config_file_path: str = os.path.join(base_dir, "configs", "user_info.json")
client_info: dict = load_data(user_config_file_path, "json")
logger.success(f"Load client info successfully:\n{json.dumps(client_info, indent=4)}")
admin_info = client_info["admin"]
student_info = client_info["student"]
teacher_info = client_info["teacher"]


# ========== User login ==========

@pytest.fixture(scope="session")
def admin():
    admin = User(ROLE.ADMIN.value, **admin_info)
    yield admin
    admin.client.logout()

@pytest.fixture(scope="session")
def teacher():
    teacher = User(ROLE.TEACHER.value, **teacher_info)
    yield teacher
    teacher.client.logout()

@pytest.fixture(scope="session")
def student():
    student = User(ROLE.STUDENT.value, **student_info)
    yield student
    student.client.logout()

@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata["Project Name"] = "My Project"
    metadata["Tester"] = "-P.A.N-"
    metadata["Project"] = "UI Automation"
    metadata["Browser"] = "Chrome"
    metadata["Environment"] = "Staging"

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    logger.success("All test cases completed.")