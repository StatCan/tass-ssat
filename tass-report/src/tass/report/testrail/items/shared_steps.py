from .item import TestRailItem, check_connection

class SharedSteps(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Shared Steps
    # Reference: https://support.testrail.com/hc/en-us/articles/7077919815572-Shared-Steps

    @check_connection
    def get_shared_step(self, shared_step_id):
        endpoint = f"get_shared_step/{shared_step_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_shared_step_history(self, shared_step_id):
        endpoint = f"get_shared_step_history/{shared_step_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_shared_steps(self, project_id, **filters):
        endpoint = self._filtered_endpoint(f"get_shared_steps/{project_id}", filters)
        return self._api_client.get(endpoint)

    @check_connection
    def add_shared_step(self, project_id, step):
        endpoint = f"add_shared_step/{project_id}"
        return self._api_client.post(endpoint, step)

    @check_connection
    def delete_shared_step(self, shared_step_id, keep=True):
        endpoint = f"delete_sharede_step/{shared_step_id}"
        return self._api_client.post(endpoint, {"keep_in_cases": 1 if keep else 0})