from .item import TestRailItem, check_connection

class BDDs(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # BDDs
    # Reference: https://support.testrail.com/hc/en-us/articles/7832161593620-BDDs

    @check_connection
    def get_bdd(self, case_id):
        endpoint = f"get_bdd/{case_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def add_bdd(self, section_id, bdd):
        endpoint = f"add_bdd/{section_id}"
        return self._api_client.post(endpoint, bdd)
