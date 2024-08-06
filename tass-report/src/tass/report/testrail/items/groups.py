from .item import TestRailItem, check_connection


class Groups(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Groups
    # References:
    # https://support.testrail.com/hc/en-us/articles/7077338821012-Groups

    @check_connection
    def get_group(self, group_id):
        endpoint = f"get_group/{group_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_groups(self):
        endpoint = "get_groups"
        return self._api_client.get(endpoint)

    @check_connection
    def add_group(self, group):
        endpoint = "add_group"
        return self._api_client.post(endpoint, group)

    @check_connection
    def update_group(self, group_id, group):
        endpoint = f"update_group/{group_id}"
        return self._api_client.post(endpoint, group)

    @check_connection
    def delete_group(self, group_id):
        endpoint = f"delete_group/{group_id}"
        return self._api_client.post(endpoint, {})
