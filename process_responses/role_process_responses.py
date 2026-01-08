import json
from apis import RoleAPI
from common import Client
from requests import Response
from typing import List, Dict, Optional
from helpers import logger_wrapper, logger
from helpers.validate_response import validate_response

class RoleProcessResponse:
    def __init__(self, client: Client = Client()) -> None:
        self.__client = client
        self.__RoleAPI = RoleAPI(self.__client)


    @logger_wrapper
    def get_all_roles(self) -> Optional[List]:
        res: Response = self.__RoleAPI.get_all_roles()
        res = validate_response(self.get_all_roles.__name__, res)
        if res is None:
            logger.warning("Get all roles failed.")
            return
        if not res:
            logger.warning("Role is empty.")
        logger.success(f"Get all roles successfully:\n{json.dumps(res, indent=4)}")
        return res

    @logger_wrapper
    def get_role_by_id(self, role_id: str = "") -> Optional[Dict]:
        res: Response = self.__RoleAPI.get_role_by_id(role_id)
        res = validate_response(self.get_role_by_id.__name__, res)
        if not res:
            logger.warning(f"Get role by id failed. Role id: '{role_id}'.")
        logger.success(f"Get role by id successfully:\n{json.dumps(res, indent=4)}")
        return res

    @logger_wrapper
    def create_new_role_with_check(self, request_body: Dict = None) -> Optional[Dict]:
        current_role_list: List = self.get_all_roles()
        if not current_role_list:
            logger.warning("Can not create new role because get all roles failed.")
            return

        for role in current_role_list:
            if role["name"] == request_body["name"]:
                logger.warning(f"Role '{request_body['name']}' already exists.")
                return role
        create_role_res: Response = self.__RoleAPI.create_role(request_body)
        create_role_res = validate_response(self.create_new_role_with_check.__name__, create_role_res)
        if create_role_res is None:
            logger.warning("Create new role failed.")
            return
        logger.success(f"Create new role successfully:\n{json.dumps(create_role_res, indent=4)}")
        return create_role_res

    @logger_wrapper
    def edit_role(self, role_id: str = "", request_body: Dict = None) -> Dict:
        res: Response = self.__RoleAPI.edit_role(role_id, request_body)
        res = validate_response(self.edit_role.__name__, res)
        if not res:
            logger.warning(f"Edit role failed. Role id: '{role_id}'.")

        logger.success(f"Edit role successfully:\n{json.dumps(res, indent=4)}")
        return res

    @logger_wrapper
    def delete_role(self, role_id: int) -> None:
        res: Response = self.__RoleAPI.delete_role(role_id)
        logger.info(f"Delete role response: {res.status_code}, {res.text}")
        return

    @logger_wrapper
    def clear_data(self, data: List = []) -> None:
        current_role_list: List = self.get_all_roles()
        if not current_role_list:
            logger.warning("Can not delete role because get all roles failed.")
            return

        for item in data:
            for current_role in current_role_list:
                if item == current_role["name"]:
                    logger.info(f"Clear data: {item}")
                    self.delete_role(current_role["_id"])

        logger.success("Complete clear data.")

