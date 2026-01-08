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
source .venv/bin/activate
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
python main.py
```
## V. Folder structure
- apis: function to call apis.
- case_setup: create predata for test cases and run cases.
    1. *_case_setup.py: create predata for test module.
    2. run_case.py: run case in data > test_cases > *_test_cases.xlsx.
- common: common class and config for create data and run case.
    1. client.py: create user instance by using data in configs > user_info.json and take action login, logout, get, post, put, patch, delete.
    2. common_setup.py: load all configs, predata setups, test case files.
    3. user.py: client instance and contains process reponse class in process_reponses > *_process_response.py.
- configs: configs using for whole project.
    1. constants.py: contains all constants.
    2. user_info.json: user infomation.
- data: contains request body templates using for create pre data and test cases for testing.
    1. request_body_template: contains detail request body for api actions and data need clear befor each running time. Each *_request_body_template.json file is used for each specific module.
    2. test_cases: contains all test cases for each module. Each *_test_cases.xlsx file is used for each specific module. Each create/ edit action needs give data (_id, name, ...) to *_request_body_template.json > need_clear field to clear created data befor running test.
- helpers: all base functions.
- logs: contain log per day.
- process_responses: contains *ProcessResponse class to process response from apis during processing predata. If create/edit action, need give data to data (_id, name, ...) to *_request_body_template.json > need_clear field to clear created data befor running test.
- reports: contains report file per day. Report is just created whenever having case runs fail.
- .env: contains environment info for project.
- main.py: main file to run project.
- README.md: project readme.
- requirements.txt: contains packages need install.

## VI. All projects in Capstone Project ecosystem
- Capstone project (cloned, using for testting purpose):
    1. Github FE: https://github.com/pannguyen2001/datn-fe
    2. Github BE: https://github.com/pannguyen2001/datn-be
    3. App: https://datn-fe-sooty.vercel.app
- Generate data tool (auto generate correct data, to save to db, reduce time prepare data):
    1. Github: https://github.com/pannguyen2001/gen_data_tool
- API testing:
    1. Github: https://github.com/pannguyen2001/api_test_cap_prj/
- UI testing using selenium:
    1. Github: (upcoming)
- Data validation:
    1. Github: https://github.com/pannguyen2001/data-da-ds-de