from tass.tools.testrail.testrail_apiclient import TestRailAPIClient



def check_connection(func):
    def wrapper(api, *args):
        breakpoint()
        if api._api_client is not None:
            func(api, *args)
        else:
            print("Not connected.")
    return wrapper


class TestRail():
    def __init__(self, user):
        self._user = user
        self._api_client = None

    def attachments(self):
        from tass.tools.testrail.items.attachments import Attachments
        return Attachments(self._api_client)

    def bdds(self):
        from tass.tools.testrail.items.attachments import BDDs
        return BDDs(self._api_client)

    def cases(self):
        from tass.tools.testrail.items.attachments import Cases
        return Cases(self._api_client)
    
    def connect(self,
                pswd,
                base_url,
                ssl_verification_level=1):
        # TODO: validate url
        if self._api_client is None:
            auth = (self._user, pswd)
            self._api_client = TestRailAPIClient(base_url,
                                                 auth,
                                                 ssl_verification_level)

    # TODO: Do something with the response
    # TODO: Validate inputs?
