from .item import TestRailItem, check_connection


class Plans(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Plans
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077711537684-Plans

    @check_connection
    def get_plan(self, plan_id):
        endpoint = f"get_plan/{plan_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_plans(self, project_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_plans/{project_id}", filters
                        )
        return self._api_client.get(endpoint)

    @check_connection
    def add_plan(self, project_id, plan):
        endpoint = f"add_plan/{project_id}"
        return self._api_client.post(endpoint, plan)

    @check_connection
    def add_plan_entry(self, plan_id, entry):
        endpoint = f"add_plan_entry/{plan_id}"
        return self._api_client.post(endpoint, entry)

    @check_connection
    def add_run_to_plan_entry(self, plan_id, entry_id, run):
        endpoint = f"add_plan_to_plan_entry/{plan_id}/{entry_id}"
        return self._api_client.post(endpoint, run)

    @check_connection
    def update_plan(self, project_id, plan):
        endpoint = f"update_plan/{project_id}"
        return self._api_client.post(endpoint, plan)

    @check_connection
    def update_plan_entry(self, plan_id, entry):
        endpoint = f"update_plan_entry/{plan_id}"
        return self._api_client.post(endpoint, entry)

    @check_connection
    def update_run_in_plan_entry(self, plan_id, entry_id, run):
        endpoint = f"update_run_in_plan_entry/{plan_id}/{entry_id}"
        return self._api_client.post(endpoint, run)

    @check_connection
    def close_plan(self, plan_id):
        endpoint = f"close_plan/{plan_id}"
        return self._api_client.post(endpoint, {})

    @check_connection
    def delete_plan(self, plan_id):
        endpoint = f"delete_plan/{plan_id}"
        return self._api_client.post(endpoint, {})

    @check_connection
    def delete_plan_entry(self, plan_id, entry_id):
        endpoint = f"delete_plan_entry/{plan_id}/{entry_id}"
        return self._api_client.post(endpoint, {})

    @check_connection
    def delete_run_from_plan_entry(self, run_id):
        endpoint = f"delete_run_from_plan_entry/{run_id}"
        return self._api_client.post(endpoint, {})
