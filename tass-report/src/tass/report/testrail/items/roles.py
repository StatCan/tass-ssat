from .item import TestRailItem, check_connection


class Roles(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Roles
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077853258772-Roles

    @check_connection
    def get_roles(self):
        endpoint = "get_roles"
        return self._api_client.get(endpoint)
