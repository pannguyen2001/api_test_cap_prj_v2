import os
import datetime
import pytz
from pathlib import Path
from os.path import join, dirname
from dotenv import load_dotenv
from enum import Enum

# =========== Load setup env from .env file ==========
dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)
LOG_FOLDER = os.getenv("LOG_FOLDER")
REPORT_FOLDER = os.getenv("REPORT_FOLDER")
BASE_URL = os.getenv("BASE_URL")
TEST_CASE_FILE_PATH = os.getenv("TEST_CASE_FILE_PATH")


# ========== Create constant data ==========
class DATETIMEFORMAT(Enum):
    DATETIME = "%Y-%m-%d %H:%M:%S"
    DATE = "%Y-%m-%d"
    DATETIME_V2 = "%Y-%m-%d_%H-%M-%S"

VN_TIME_ZONE = pytz.timezone("Asia/Ho_Chi_Minh")
today = datetime.datetime.now().astimezone(VN_TIME_ZONE).strftime(DATETIMEFORMAT.DATE.value)
datetime_today = datetime.datetime.now().astimezone(VN_TIME_ZONE).strftime(DATETIMEFORMAT.DATETIME.value)



# ========== Create log file ===========
log_file_name = f"{today}.log"
log_file_path = os.path.join(LOG_FOLDER, log_file_name)
log_file_path = Path(log_file_path)
log_file_path.parent.mkdir(exist_ok=True, parents=True)

# ========== Create report file ===========
report_file_name = f"{datetime_today}.xlsx"
report_file_path = os.path.join(REPORT_FOLDER, report_file_name)
report_file_path = Path(report_file_path)
report_file_path.parent.mkdir(exist_ok=True, parents=True)

# ========== Enum class ===========
class MODULETEST(Enum):
    ROLE = "role"
    ACCOUNT = "account"
    STUDENT = "student"
    TEACHER = "teacher"
    COURSE_CATEGORY = "course_category"
    COURSE = "course"

class ROLE(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"

class APIMETHOD(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

class FILETYPE(Enum):
    JSON = "json"
    TEXT = "txt"
    CSV = "csv"
    EXCEL = "xlsx"

FILE_TYPE = list(map(lambda c: c.value, FILETYPE))


