from .item import TestRailItem, check_connection

class Projects(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Projects
    # Reference: https://support.testrail.com/hc/en-us/articles/7077792415124-Projects

    @check_connection
    def get_project(self, project_id):
        endpoint = f"get_project/{project_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_projects(self, **filters):
        endpoint = self._filtered_endpoint("get_projects", filters)
        return self._api_client.get(endpoint)

    @check_connection
    def add_project(self, project):
        endpoint = "add_project"
        return self._api_client.post(endpoint, project)

    @check_connection
    def update_project(self, project_id, project):
        endpoint = f"update_project/{project_id}"
        return self._api_client.post(endpoint, project)

    @check_connection
    def delete_project(self, project_id):
        endpoint = f"delete_project/{project_id}"
        return self._api_client.post(endpoint, {})