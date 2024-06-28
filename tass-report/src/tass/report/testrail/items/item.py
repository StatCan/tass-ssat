def check_connection(func):
    def wrapper(api, *args, **kwargs):
        if api._api_client is not None:
            return func(api, *args, **kwargs)
        else:
            print("Not connected.")
    return wrapper


class TestRailItem():

    def _filtered_endpoint(self, endpoint, filters):
        _endpoint = endpoint
        for param, value in filters.items():
            _endpoint += f"&{param}={value}"
        return _endpoint