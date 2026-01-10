# API test for capstone project - version 2: apply pytest and allure report
- Created by: Pham Anh Nhat
- Created on: 2026-01-07
- Last modified on: 2026-01-08
- Version: 1.0.0
- Status: Not complete.

## I. Aim
- Testing API for capstone project, for learning pytest.

## II. Technology and packages
- Python: 3.11.10
- Pytest: 9.0.2
- Requests: 2.32.5
- Loguru: 0.7.3

## III. Capstone project infomation:
- Github: <datn-fe-pannguyen>
- Website: https://datn-fe-sooty.vercel.app/
- Manual test: 

## IV. Guideline
1. Install virtual env
```
python -m venv .venv
```
2. Activate venv
```
source .venv/bin/activate or .venv/Scripts/Activate.ps1
```
3. Check python version
```
python --version
```
4. Installnecessary package in requirements.txt file
```
pip install -r requirements.txt
```
5. Check package installed and its version
```
pip list
```
6. .env folder
```
LOG_FOLDER = <your_real_path>/logs
REPORT_FOLDER = <your_real_path>/reports
BASE_URL = <app_url>
TEST_CASE_FILE_PATH = <your_real_path>/data/test_cases/account_test_cases.xlsx
```
7. Run project
```
# if just run:
python main.py or pytest -m <mark> or pytest testcases/<test_file_name>.py
# if want to run with report, run with commands below step by step:
pytest --alluredir=allure-results --clean-alluredir
allure generate allure-results -o allure-report --clean
allure serve allure-results
```

## V. All projects in Capstone Project ecosystem
- Capstone project (cloned, using for testting purpose):
    1. Github FE: https://github.com/pannguyen2001/datn-fe
    2. Github BE: https://github.com/pannguyen2001/datn-be
    3. App: https://datn-fe-sooty.vercel.app
- Generate data tool (auto generate correct data, to save to db, reduce time prepare data):
    1. Github: https://github.com/pannguyen2001/gen_data_tool
- API testing:
    1. Github: https://github.com/pannguyen2001/api_test_cap_prj/
- API testing v2 (combine pytest and allure report):
    1. Github: https://github.com/pannguyen2001/api_test_cap_prj_v2
- UI testing using selenium:
    1. Github: (upcoming)