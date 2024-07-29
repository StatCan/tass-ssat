from .item import TestRailItem, check_connection


class Cases(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # API endpoint utilities linked to cases

    def case_fields(self):
        return CaseFields(self._api_client)

    def case_types(self):
        return CaseTypes(self._api_client)

    # Cases
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077292642580-Cases

    @check_connection
    def get_case(self, case_id):
        endpoint = f"get_case/{case_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_cases(self, project_id, suite_id=None, **filters):
        endpoint = f"get_cases/{project_id}"
        if suite_id:
            endpoint += f"&suite_id={suite_id}"
        endpoint = self._filtered_endpoint(endpoint, filters)
        return self._api_client.get(endpoint)

    @check_connection
    def get_history_for_case(self, case_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_history_for_case/{case_id}", filters
                        )
        return self._api_client.get(endpoint)

    @check_connection
    def add_case(self, section_id, case):
        endpoint = f"add_case/{section_id}"
        return self._api_client.post(endpoint, case)

    @check_connection
    def copy_cases_to_section(self, section_id, cases):
        endpoint = f"copy_cases_to_section/{section_id}"
        return self._api_client.post(endpoint, cases)

    @check_connection
    def update_case(self, case_id, case):
        endpoint = f"update_case/{case_id}"
        return self._api_client.post(endpoint, case)

    @check_connection
    def update_cases(self, suite_id, cases):
        endpoint = f"update_cases/{suite_id}"
        return self._api_client.post(endpoint, cases)

    @check_connection
    def move_cases_to_section(self, section_id, cases):
        endpoint = f"move_cases_to_section/{section_id}"
        return self._api_client.post(endpoint, cases)

    @check_connection
    def delete_case(self, case_id, soft=False):
        endpoint = f"delete_case/{case_id}"
        return self._api_client.post(endpoint, {"soft": 1 if soft else 0})

    @check_connection
    def delete_cases(self, suite_id, cases, soft=False):
        endpoint = f"delete_cases/{suite_id}"
        _delete = {"case_ids": cases, "soft": 1 if soft else 0}
        return self._api_client.post(endpoint, _delete)


class CaseFields(Cases):
    def __init__(self, api):
        self._api_client = api

    # Case Fields
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077281158164-Case-Fields

    @check_connection
    def get_case_fields(self):
        endpoint = "get_case_fields"
        return self._api_client.get(endpoint)

    @check_connection
    def add_case_field(self, field):
        endpoint = "add_case_field"
        return self._api_client.post(endpoint, field)


class CaseTypes(Cases):
    def __init__(self, api):
        self._api_client = api

    # Case Types
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077295487252-Case-Types

    @check_connection
    def get_case_types(self):
        endpoint = "get_case_types"
        return self._api_client.get(endpoint)
