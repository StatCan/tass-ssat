from .item import TestRailItem, check_connection

class Priorities(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Priorities
    # Reference: https://support.testrail.com/hc/en-us/articles/7077746564244-Priorities

    @check_connection
    def get_priorities(self):
        endpoint = "get_priorities"
        return self._api_client.get(endpoint)