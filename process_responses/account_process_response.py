import json
from apis import AccountAPI
from common import Client
from requests import Response
from typing import List, Dict, Optional
from helpers.logger_wrapper import logger_wrapper
from helpers.logger import logger
from helpers.validate_response import validate_response
from helpers.time_execution_wrapper import time_execution_wrapper


class AccountResponse:
    def __init__(self, client: Client = Client()) -> None:
        self.__client = client
        self.__AccountAPI = AccountAPI(self.__client)

    @logger_wrapper
    @time_execution_wrapper
    def get_all_accounts(self) -> Optional[List]:
        res: Response = self.__AccountAPI.get_all_accounts()
        res = validate_response(self.get_all_accounts.__name__, res)
        if res is None:
            logger.warning("Get all accounts failed.")
            return
        if not res:
            logger.warning("Account is empty.")
        return res

    @logger_wrapper
    @time_execution_wrapper
    def get_account_by_id(self, account_id: str = "") -> None:
        res: Response = self.__AccountAPI.get_account_by_id(account_id)
        res = validate_response(self.get_account_by_id.__name__, res)
        if not res:
            logger.warning(f"Get account by id failed. Account id: '{account_id}'.")
        logger.success(f"Get account by id successfully:\n{json.dumps(res, indent=4)}")
        return res

    @logger_wrapper
    @time_execution_wrapper
    def create_new_account_with_check(self, request_body: Dict = None) -> Optional[Dict]:
        current_account_list: List = self.get_all_accounts()
        if not current_account_list:
            logger.warning("Can not create new account because get all accounts failed.")
            return

        for account in current_account_list:
            if account["email"] == request_body["email"]:
                logger.warning(f"Account with email: '{request_body['email']}' already exists.")
                return account
            if account["full_name"] == request_body["full_name"]:
                logger.warning(f"Account with full_name: '{request_body['full_name']}' already exists.")
                return account

        create_account_res: Response = self.__AccountAPI.create_account(request_body)
        create_account_res = validate_response(self.create_new_account_with_check.__name__, create_account_res)
        if create_account_res is None:
            logger.warning("Create new account failed.")
            return
        logger.success(f"Create new account successfully:\n{json.dumps(create_account_res, indent=4)}")
        return create_account_res

    @logger_wrapper
    def edit_account(self, account_id: str = "", request_body: Dict = None) -> Dict:
        res: Response = self.__AccountAPI.edit_account(account_id, request_body)
        res = validate_response(self.edit_account.__name__, res)
        if not res:
            logger.warning(f"Edit account failed. Account id: '{account_id}'.")

        logger.success(f"Edit account successfully:\n{json.dumps(res, indent=4)}")
        return res

    @logger_wrapper
    def delete_account(self, account_id: str = "") -> None:
        res: Response = self.__AccountAPI.delete_account(account_id)
        logger.info(f"Delete account response: {res.status_code}")
        return

    @logger_wrapper
    def clear_data(self, data: List = []) -> None:
        current_account_list: List = self.get_all_accounts()
        if not current_account_list:
            logger.warning("Can not delete account because get all account failed.")
            return

        for item in data:
            for current_account in current_account_list:
                if item == current_account["full_name"]:
                    logger.info(f"Clear data: {item}")
                    self.delete_account(current_account["_id"])

        logger.success("Complete clear data.")