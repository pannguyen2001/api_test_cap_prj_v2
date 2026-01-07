from .client import Client
from process_responses import RoleProcessResponse, AccountResponse

class User:
    def __init__(
        self,
        role: str = "",
        email: str = "",
        password: str = "",
        *args,
        **kwargs
        ) -> None:
        self.client = Client(role, email, password, *args, **kwargs)
        self.AccountResponse = AccountResponse(self.client)
        self.RoleProcessResponse = RoleProcessResponse(self.client)
        self.client.login()

    def post(self, url, data=None):
        return self.client.post(url, json=data)

    def put(self, url, data=None):
        return self.client.put(url, json=data)

    def get(self, url):
        return self.client.get(url)

    def delete(self, url, data=None):
        return self.client.delete(url, json=data)

