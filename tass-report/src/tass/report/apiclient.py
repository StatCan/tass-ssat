import requests


class APIClient():
    def __init__(self,
                 base_url,
                 auth,
                 ssl_verification_level=1):
        if not base_url.endswith('/'):
            base_url += '/'
        self.__base_url = base_url
        s = requests.Session()
        match ssl_verification_level:
            case 1 | '1':
                # default. Verify is true
                s.verify = True
            case 2 | '2':
                # Verify using local certificate
                s.cert = ''  # TODO: Get certificate path somewhere
            case 3 | '3':
                # Do not verify certificate
                s.verify = False
            case _:
                print("Not a recognized level. Using default.")
                s.verify = True
        s.auth = auth
        self._session = s

    @property
    def url(self):
        return self.__base_url

    def start_request(self, endpoint, **kwargs):
        url = self.__base_url + "/" + endpoint
        return requests.Request(url=url, **kwargs)

    def send_request(self, request):
        r = self._session.prepare_request(request)
        response = self._session.send(r)
        # TODO: check response status/error messages
        return response

    def _handle_response(self, response):
        with response:
            if (response.status_code == 200):
                return response.json()
            elif (response.status_code >= 400):
                # TODO: report error
                return {"status": f"{response.status_code}: {response.reason}",
                        "message": response.text}
            else:
                # TODO: unexpected response, implementation?
                # Unexpected response
                return response


class APIException(Exception):
    # TODO: Expand on this exception
    pass
