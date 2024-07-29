from .item import TestRailItem, check_connection


class Tests(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Tests
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077990441108-Tests

    @check_connection
    def get_test(self, test_id, **filters):
        endpoint = self._filtered_endpoint(f"get_test/{test_id}", filters)
        return self._api_client.get(endpoint)

    @check_connection
    def get_tests(self, run_id, **filters):
        endpoint = self._filtered_endpoint(f"get_tests/{run_id}", filters)
        return self._api_client.get(endpoint)
