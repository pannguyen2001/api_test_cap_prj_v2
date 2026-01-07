"""

"""
import json
import pytest
import os
from typing import Dict
from helpers import logger
from helpers import load_data
from .user import User
from configs.constants import ROLE

logger.info(f"{' Load common info and setup ':=^50}")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger.info(f"Base dir: {base_dir}")

# ========== Load predata ===========
# Role
@pytest.fixture
def role_predata_info():
    role_request_body_template_file_path: str = os.path.join(base_dir, "data", "request_body_template", "role_request_body_template.json")
    role_predata_info: Dict = load_data(role_request_body_template_file_path, "json")
    logger.success(f"Load role predata successfully:\n{json.dumps(role_predata_info, indent=4)}")
    return role_predata_info

# Account
@pytest.fixture
def account_predata_info():
    account_request_body_template_file_path: str = os.path.join(base_dir, "data", "request_body_template", "account_request_body_template.json")
    account_predata_info: Dict = load_data(account_request_body_template_file_path, "json")
    logger.success(f"Load account predata successfully:\n{json.dumps(account_predata_info, indent=4)}")
    return account_predata_info


# =========== Load client info from USER_CONFIG_FILE_PATH ==========
user_config_file_path: str = os.path.join(base_dir, "configs", "user_info.json")
client_info: dict = load_data(user_config_file_path, "json")
logger.success(f"Load client info successfully:\n{json.dumps(client_info, indent=4)}")

@pytest.fixture
def admin_info():
    return client_info["admin"]

@pytest.fixture
def student_info():
    return client_info["student"]

@pytest.fixture
def teacher_info():
    return client_info["teacher"]


# ========== User login ==========
@pytest.fixture
def admin():
    return User(ROLE.ADMIN.value, **admin_info)

@pytest.fixture
def student():
    return User(ROLE.STUDENT.value, **student_info)

@pytest.fixture
def teacher():
    return User(ROLE.TEACHER.value, **teacher_info)


@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata["Project Name"] = "My Project"
    metadata["Tester"] = "-P.A.N-"
    metadata["Project"] = "UI Automation"
    metadata["Browser"] = "Chrome"
    metadata["Environment"] = "Staging"