from .item import TestRailItem, check_connection

class Statuses(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Status
    # Reference: https://support.testrail.com/hc/en-us/articles/7077935129364-Statuses

    @check_connection
    def get_case_statuses(self):
        endpoint = "get_case_statuses"
        return self._api_client.get(endpoint)

    @check_connection
    def get_statuses(self):
        endpoint = "get_statuses"
        return self._api_client.get(endpoint)