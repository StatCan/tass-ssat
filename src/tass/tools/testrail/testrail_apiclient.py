import json
from tass.tools.apiclient import APIClient

class TestRailAPIClient(APIClient):
    def __init__(self,
                 base_url,
                 auth,
                 ssl_verification_level=1):
        if base_url.endswith("/"):
            base_url += "index.php?/api/v2/"
        else:
            base_url += "/index.php?/api/v2/"
        super().__init__(base_url,
                         auth,
                         ssl_verification_level)
                         
    def _handle_response(self, response):
        with response:
            if (response.status_code == 200):
                return response.json()
            elif (response.status_code >= 400):
                # TODO: report error
                return {"status": f"{response.status_code}: {response.reason}",
                        "message": response.text['error']}
                }
            elif:
                # TODO: unexpected response, implementation?
                # Unexpected response
                return response
            

    def get(self, endpoint):
        _request = self.start_request(endpoint, method="GET")
        _request.headers['Content-Type'] = 'application/json'
        response = self.send_request(_request)
        return self._handle_response(response)           

    def post(self, endpoint, payload):
        _request = self.start_request(endpoint, method="POST")
        _request.headers['Content-Type'] = 'application/json'
        _request.data = bytes(json.dumps(payload or {}), 'utf-8')
        response = self.send_request(_request)
        return self._handle_response(response)   

    def post_attachment(self, endpoint, attachment):
        _request = self.start_request(endpoint, method='POST')
        _request.headers['Content-Type'] = 'multipart/form-data'
        with open(attachment, 'rb') as f:
            _attachment = {'attachment': f}
        _request.files = _attachment
        response = self.send_request(_request)
        return self._handle_response(response)
