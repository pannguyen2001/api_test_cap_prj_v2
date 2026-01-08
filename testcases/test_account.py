import pytest
from typing import List
from helpers.load_data import load_data
from helpers.run_case import run_case
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
account_test_cases: List = load_data(BASE_DIR / "data/test_cases/account_test_cases.xlsx")
account_test_cases = [i for i in account_test_cases if i["status"] == "Done"]

@pytest.mark.account
@pytest.mark.parametrize("test_cases", account_test_cases, ids=[i["case_no"] for i in account_test_cases])
def test_account(test_cases, account_case_setup, admin, student, teacher):
    run_case(
        admin,
        student,
        teacher,
        test_cases,
        pre_data=account_case_setup
    )

