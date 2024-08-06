from .item import TestRailItem, check_connection


class Reports(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Reports
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077825062036-Reports

    @check_connection
    def get_reports(self, project_id):
        endpoint = f"get_reports/{project_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def run_report(self, report_template_id):
        endpoint = f"run_report/{report_template_id}"
        return self._api_client.get(endpoint)
