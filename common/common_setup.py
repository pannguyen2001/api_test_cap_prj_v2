"""

"""
import json
import os
from typing import Dict
from helpers import logger
from helpers import load_data
import dotenv

dotenv.load_dotenv()

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

# =========== Load client info from USER_INFO ==========
# user_config_file_path: str = os.path.join(base_dir, "configs", "user_info.json")
# logger.info(os.getenv("USER_INFO"))
client_info: dict = json.loads(os.getenv("USER_INFO"))
logger.success("Load client info successfully")
# load_data(user_config_file_path, "json")
admin_info: dict = client_info["admin"]
student_info: dict = client_info["student"]
teacher_info: dict = client_info["teacher"]


# ========== User login ==========
# admin: User = User(ROLE.ADMIN.value, **admin_info)
# student: User = User(ROLE.STUDENT.value, **student_info)
# teacher: User = User(ROLE.TEACHER.value, **teacher_info)