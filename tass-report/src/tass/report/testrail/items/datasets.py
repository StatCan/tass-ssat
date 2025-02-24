from .item import TestRailItem, check_connection


class DataSets(TestRailItem):
    def __init__(self, api):
        self._api_client = api

    # Datasets
    # Reference:
    # https://support.testrail.com/hc/en-us/articles/7077300491540-Datasets

    @check_connection
    def get_dataset(self, dataset_id):
        endpoint = f"get_dataset/{dataset_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def get_datasets(self, project_id):
        endpoint = f"get_datasets/{project_id}"
        return self._api_client.get(endpoint)

    @check_connection
    def add_dataset(self, project_id, dataset):
        endpoint = f"add_dataset/{project_id}"
        return self._api_client.post(endpoint, dataset)

    @check_connection
    def update_dataset(self, dataset_id, dataset):
        endpoint = f"update_dataset/{dataset_id}"
        return self._api_client.post(endpoint, dataset)

    @check_connection
    def delete_dataset(self, dataset_id):
        endpoint = f"delete_dataset/{dataset_id}"
        return self._api_client.post(endpoint, {})
