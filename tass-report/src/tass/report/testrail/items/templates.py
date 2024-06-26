from .item import TestRailItem, check_connection

class Templates(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Templates
    # Reference: https://support.testrail.com/hc/en-us/articles/7077938165780-Templates

    @check_connection
    def get_templates(self, project_id):
        endpoint = f"get_templates/{project_id}"
        return self._api_client.get(endpoint)