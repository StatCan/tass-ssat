from .item import TestRailItem, check_connection

class Runs(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Runs
    # Reference: https://support.testrail.com/hc/en-us/articles/7077874763156-Runs

    @check_connection
    def get_run(self, run_id):
        endpoint = f"get_run/{get_run}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_runs(self, project_id, **filters):
        endpoint = self._filtered_endpoint(f"get_runs/{project_id}", filters)
        return self._api_client.get(endpoint)

    @check_connection
    def add_run(self, project_id, run):
        endpoint = f"add_run/{project_id}"
        return self._api_client.post(endpoint, run)

    @check_connection
    def update_run(self, run_id, run):
        endpoint = f"update_run/{run_id}"
        return self._api_client.post(endpoint, run)

    @check_connection
    def close_run(self, run_id):
        endpoint = f"close_run/{run_id}"
        return self._api_client.post(endpoint, {})

    @check_connection
    def delete_run(self, run_id, soft=False):
        endpoint = f"delete_run/{run_id}"
        return self._api_client.post(endpoint, {"soft": 1 if soft else 0})