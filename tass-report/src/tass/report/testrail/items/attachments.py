from .item import TestRailItem, check_connection


class Attachments(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Attachments
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077196481428-Attachments

    @check_connection
    def add_attachment_to_case(self, case_id, attachment):
        endpoint = f"add_attachment_to_case/{case_id}"
        return self._api_client.post_attachment(endpoint, attachment)

    @check_connection
    def add_attachment_to_plan(self, plan_id, attachment):
        endpoint = f"add_attachment_to_plan/{plan_id}"
        return self._api_client.post_attachment(endpoint, attachment)

    @check_connection
    def add_attachment_to_plan_entry(self, plan_id, entry_id, attachment):
        endpoint = f"add_attachment_to_plan_entry/{plan_id}/{entry_id}"
        return self._api_client.post_attachment(endpoint, attachment)

    @check_connection
    def add_attachment_to_result(self, result_id, attachment):
        endpoint = f"add_attachment_to_result/{result_id}"
        return self._api_client.post_attachment(endpoint, attachment)

    @check_connection
    def add_attachment_to_run(self, run_id, attachment):
        endpoint = f"add_attachment_to_run/{run_id}"
        return self._api_client.post_attachment(endpoint, attachment)

    @check_connection
    def get_attachments_for_case(self, case_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_attachments_for_case/{case_id}", filters
                        )
        return self._api_client.get(endpoint)

    @check_connection
    def get_attachments_for_plan(self, plan_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_attachments_for_plan/{plan_id}", filters
                        )
        return self._api_client.get(endpoint)

    @check_connection
    def get_attachments_for_plan_entry(self, plan_id, entry_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_attachments_for_plan_entry/{plan_id}/{entry_id}",
                        filters
                        )
        return self._api_client.get(endpoint)

    @check_connection
    def get_attachments_for_run(self, run_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_attachments_for_run/{run_id}", filters
                        )
        return self._api_client.get(endpoint)

    @check_connection
    def get_attachments_for_test(self, test_id, **filters):
        endpoint = self._filtered_endpoint(
                        f"get_attachments_for_test/{test_id}", filters
                        )
        return self._api_client.get(endpoint)

    @check_connection
    def get_attachment(self, attachment_id):
        endpoint = f"get_attachment/{attachment_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def delete_attachment(self, attachment_id):
        endpoint = f"delete_attachment/{attachment_id}"
        return self._api_client.post(endpoint, None)
