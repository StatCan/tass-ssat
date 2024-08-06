from .item import TestRailItem, check_connection


class Sections(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Sections
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077918603412-Sections

    @check_connection
    def get_section(self, section_id):
        endpoint = f"get_section/{section_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_sections(self, project_id, suite_id=None, **filters):
        endpoint = f"get_sections/{project_id}"
        if suite_id:
            endpoint += f"&suite_id={suite_id}"
        endpoint = self._filtered_endpoint(endpoint, filters)
        return self._api_client.get(endpoint)

    @check_connection
    def add_section(self, project_id, section):
        endpoint = f"add_section/{project_id}"
        return self._api_client.post(endpoint, section)

    @check_connection
    def move_section(self, section_id, section):
        endpoint = f"move_section/{section_id}"
        return self._api_client.post(endpoint, section)

    @check_connection
    def update_section(self, section_id, section):
        endpoint = f"update_section/{section_id}"
        return self._api_client.post(endpoint, section)

    @check_connection
    def delete_section(self, section_id, soft=False):
        endpoint = f"delete_section/{section_id}"
        return self._api_client.post(endpoint,
                                     {"soft": 1 if soft else 0})
