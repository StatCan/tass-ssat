from .item import TestRailItem, check_connection

class Configurations(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Configurations
    # Reference: https://support.testrail.com/hc/en-us/articles/7077298488340-Configurations

    @check_connection
    def get_configs(self, project_id):
        endpoint = f"get_configs/{project_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def add_config_group(self, project_id, name):
        endpoint = f"add_config_group/{project_id}"
        return self._api_client.post(endpoint, {"name": name})

    @check_connection
    def add_config(self, config_group_id, name):
        endpoint = f"add_config/{config_group_id}"
        return self._api_client.post(endpoint, {"name": name})

    @check_connection
    def update_config_group(self, config_group_id, name):
        endpoint = f"update_config_group/{config_group_id}"
        return self._api_client.post(endpoint, {"name": name})

    @check_connection
    def update_config(self, config_id, name):
        endpoint = f"update_config/{config_id}"
        return self._api_client.post(endpoint, {"name": name})

    @check_connection
    def delete_config_group(self, config_group_id):
        endpoint = f"delete_config_group/{config_group_id}"
        return self._api_client.post(endpoint, {})

    @check_connection
    def delete_config(self, config_id):
        endpoint = f"delete_config/{config_id}"
        return self._api_client.post(endpoint, {})