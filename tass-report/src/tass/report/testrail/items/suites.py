from .item import TestRailItem, check_connection


class Suites(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Suites
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077936624276-Suites

    @check_connection
    def get_suite(self, suite_id):
        endpoint = f"get_suite/{suite_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_suites(self, project_id):
        endpoint = f"get_suites/{project_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def add_suite(self, project_id, suite):
        endpoint = f"add_suite/{project_id}"
        return self._api_client.post(endpoint, suite)

    @check_connection
    def update_suite(self, suite_id, suite):
        endpoint = f"update_suite/{suite_id}"
        return self._api_client.post(endpoint, suite)

    @check_connection
    def delete_suite(self, suite_id, soft=False):
        endpoint = f"delete_suite/{suite_id}"
        return self._api_client.post(endpoint, {"soft": 1 if soft else 0})
