from .item import TestRailItem, check_connection


class Results(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # API endpoint utilities related to Results

    def result_fields(self):
        return Results.ResultFields(self._api_client)

    # Results
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077819312404-Results

    @check_connection
    def get_results(self, test_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_results/{test_id}", filters
                        )
        return self._api_client.get(endpoint)

    @check_connection
    def get_results_for_case(self, run_id, case_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_results_for_case/{run_id}/{case_id}", filters
                        )
        return self._api_client().get(endpoint)

    @check_connection
    def get_results_for_run(self, run_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_results_for_run/{run_id}", filters
                        )
        return self._api_client().get(endpoint)

    @check_connection
    def add_result(self, test_id, result):
        endpoint = f"add_result/{test_id}"
        return self._api_client.post(endpoint, result)

    @check_connection
    def add_result_for_case(self, run_id, case_id, result):
        endpoint = f"add_result_for_case/{run_id}/{case_id}"
        return self._api_client.post(endpoint, result)

    @check_connection
    def add_results(self, run_id, results):
        endpoint = f"add_results/{run_id}"
        return self._api_client.post(endpoint, results)

    @check_connection
    def add_results_for_cases(self, run_id, results):
        endpoint = f"add_results_for_cases/{run_id}"
        return self._api_client.post(endpoint, results)

    class ResultFields(TestRailItem):
        def __init__(self, api):
            self._api_client = api

        # Result Fields
        # Reference:
        # https://support.testrail.com/hc/en-us/articles/7077871398036-Result-Fields

        @check_connection
        def get_result_fields(self):
            endpoint = "get_result_fields"
            return self._api_client.get(endpoint)
