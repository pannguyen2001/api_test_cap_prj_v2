import pytest
from typing import List
from helpers.load_data import load_data
from helpers.run_case import run_case

role_test_cases: List = load_data("/home/user/apitestcapprj/data/test_cases/role_test_cases.xlsx")
role_test_cases = [i for i in role_test_cases if i["status"] == "Done"]

@pytest.mark.role
@pytest.mark.parametrize("test_cases", role_test_cases, ids=[i["case_no"] for i in role_test_cases])
def test_role(test_cases, role_case_setup, admin, student, teacher):
    run_case(
        admin,
        student,
        teacher,
        test_cases,
        pre_data=role_case_setup
    )

