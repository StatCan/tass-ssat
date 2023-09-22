class TestRailItem():

    def _filtered_endpoint(self, endpoint, filters):
        _endpoint = endpoint
        for param, value in filters.items():
            _endpoint += f"&{param}={value}"
        return _endpoint