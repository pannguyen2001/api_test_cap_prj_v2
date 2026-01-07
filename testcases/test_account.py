


import pytest
from case_setup.base_test import BaseTest
from configs.constants import TEST_CASE_FILE_PATH
from case_setup.account_case_setup import account_case_setup


@pytest.mark.account
class TestAccountCaseSetup(BaseTest):

    def test_account_case_setup(self, account_case_setup):
        self.setup_test("Account")
        self.run_test(
            test_case_file_path="/home/user/apitestcapprj/data/test_cases/account_test_cases.xlsx",
            pre_data=account_case_setup
        )
        self.tear_down()
