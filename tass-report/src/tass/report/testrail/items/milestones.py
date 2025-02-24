from .item import TestRailItem, check_connection


class Milestones(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Milestones
    # References:
    # https://support.testrail.com/hc/en-us/articles/7077723976084-Milestones

    @check_connection
    def get_milestone(self, milestone_id):
        endpoint = f"get_milestone/{milestone_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_milestones(self, project_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_milestones/{project_id}", filters
                        )
        return self._api_client.get(endpoint)

    @check_connection
    def add_milestone(self, project_id, milestone):
        endpoint = f"add_milestone/{project_id}"
        return self._api_client.post(endpoint, milestone)

    @check_connection
    def update_milesonte(self, milestone_id, milestone):
        endpoint = f"update_milestone/{milestone_id}"
        return self._api_client.post(endpoint, milestone)

    @check_connection
    def delete_milestone(self, milestone_id):
        endpoint = f"delete_milestone/{milestone_id}"
        return self._api_client.post(endpoint, {})
