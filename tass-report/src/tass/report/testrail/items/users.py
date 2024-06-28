from .item import TestRailItem, check_connection

class Users(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Users
    # Reference: https://support.testrail.com/hc/en-us/articles/7077978310292-Users

    @check_connection
    def get_user(self, user_id):
        endpoint = f"get_user/{user_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_current_user(self):
        endpoint = "get_current_user"
        return self._api_client.get(endpoint)
    
    @check_connection
    def get_user_by_email(self, email):
        endpoint = f"get_user_by_email&email={email}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_users(self, project_id=None):
        endpoint = "get_users"
        if project_id is not None:
            endpoint += f"/{project_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def add_user(self, user):
        endpoint = "add_user"
        return self._api_client.post(endpoint, user)

    @check_connection
    def update_user(self, user_id, user):
        endpoint = f"update_user/{user_id}"
        return self._api_client.post(endpoint, user)