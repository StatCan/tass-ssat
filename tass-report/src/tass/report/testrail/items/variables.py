from .item import TestRailItem, check_connection


class Variables(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Variables
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077979742868-Variables

    @check_connection
    def get_variables(self, project_id):
        endpoint = f"get_variables/{project_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def add_variable(self, project_id, variable):
        endpoint = f"add_variable/{project_id}"
        return self._api_client.post(endpoint, variable)

    @check_connection
    def update_variable(self, variable_id, variable):
        endpoint = f"update_variable/{variable_id}"
        return self._api_client.post(endpoint, variable)

    @check_connection
    def delete_variable(self, variable_id):
        endpoint = f"delete_variable/{variable_id}"
        return self._api_client.post(endpoint, {})
