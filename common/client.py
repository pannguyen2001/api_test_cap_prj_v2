import requests
from requests import Response, get, post, put, patch, delete
from typing import Dict, Literal
from configs.constants import BASE_URL
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
from helpers import retry, logger
from helpers.validate_response import validate_response

ROLE_TYPE = Literal["admin", "student", "teacher"]

class Client:
    def __init__(
        self,
        role: ROLE_TYPE = "admin",
        email: str = "",
        password: str = "",
        base_url: str = BASE_URL,
        *args,
        **kwargs
        ) -> None:
            self.__role = role
            self.__email = email
            self.__password = password
            self.__base_url = base_url
            self.__header = {
                "Token": ""
            }
            self.__info = None
            self.session = requests.session()
            self.session.mount("http://", HTTPAdapter(max_retries=Retry(total=3, allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "PATCH"]))))

    def get_role(self) -> str:
        return self.__role

    def set_role(self, role: str = "") -> None:
        self.__role = role

    def get_email(self) -> str:
        return self.__email

    def set_email(self, email: str = "") -> None:
        self.__email = email

    def get_password(self) -> str:
        return self.__password

    def set_password(self, password: str = "") -> None:
        self.__password = password

    def get_base_url(self) -> str:
        return self.__base_url

    def set_base_url(self, base_url: str = "") -> None:
        self.__base_url = base_url

    def get_header(self) -> Dict:
        return self.__header

    def set_header(self, header: Dict = None) -> None:
        self.__header = header

    def assign_url(self, url: str = "") -> str:
        if not url.startswith("https://") or not url.startswith("http://"):
            return f"{self.__base_url}{url}"
        return url

    def get(
        self,
        url: str = "",
        json: Dict = None,
        *args,
        **kwargs
        ) -> Response:
        url: str = self.assign_url(url)
        return get(
            url,
            headers=self.__header,
            json=json,
            *args,
            **kwargs
            )

    def post(
        self,
        url: str = "",
        json: Dict = None,
        *args,
        **kwargs
        ) -> Response:
        url: str = self.assign_url(url)
        return post(
            url,
            headers=self.__header,
            json=json,
            *args,
            **kwargs
            )

    def put(
        self,
        url: str = "",
        json: Dict = None,
        *args,
        **kwargs
        ) -> Response:
        url: str = self.assign_url(url)
        return put(
            url,
            headers=self.__header,
            json=json,
            *args,
            **kwargs
            )

    def patch(
        self,
        url: str = "",
        json: Dict = None,
        *args,
        **kwargs
        ) -> Response:
        url: str = self.assign_url(url)
        return patch(
            url,
            headers=self.__header,
            json=json,
            *args,
            **kwargs
            )

    def delete(self,
        url: str = "",
        json: Dict = None,
        *args,
        **kwargs
        ) -> Response:
        url: str = self.assign_url(url)
        return delete(
            url,
            headers=self.__header,
            json=json,
            *args,
            **kwargs
            )

    @retry(3)
    def login(self):
        logger.info(f"Login with role: {self.__role}, email: {self.__email} and password: {self.__password}.")
        request_body: Dict = {
            "email": self.__email,
            "password": self.__password
        }
        res: Response = self.post("/api/auth/login", json=request_body)
        res = validate_response(self.login.__name__, res)
        if not res:
            logger.warning("Login failed.")
            return
        self.__header["Token"] = f"Bearer {res.get('accessToken', '')}"
        self.__info = res
        logger.success("Login successfully.")

    @retry(3)
    def logout(self):
        logger.info(f"User: '{self.__email}', role: '{self.__role}' logout.")
        res: Response = self.post("/api/auth/logout")
        logger.info(f"Logout info: {res.status_code}, {res.text}.")