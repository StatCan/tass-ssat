from .apiclient import TestRailAPIClient
from . import items


class TestRail():
    def __init__(self, user):
        self._user = user
        self._api_client = None

    # Testrail api endpoint utility functions
    # each functions returns a testrail item that manages endpoints for each type
    
    def attachments(self):
        return items.Attachments(self._api_client)

    def bdds(self):
        return items.BDDs(self._api_client)

    def cases(self):
        return items.Cases(self._api_client)
        
    def configurations(self):
        return items.Configurations(self._api_client)
        
    def groups(self):
        return items.Groups(self._api_client)
        
    def milestones(self):
        return items.Milestones(self._api_client)
        
    def plans(self):
        return items.Plans(self._api_client)
        
    def priorities(self):
        return items.Priorities(self._api_client)

    def projects(self):
        breakpoint()
        return items.Projects(self._api_client)
        
    def reports(self):
        return items.Reports(self._api_client)
        
    def results(self):
        return items.Results(self._api_client)
        
    def roles(self):
        return items.Roles(self._api_client)
        
    def runs(self):
        return items.Runs(self._api_client)
        
    def sections(self):
        return items.Sections(self._api_client)
        
    def shared_steps(self):
        return items.SharedSteps(self._api_client)
        
    def statuses(self):
        return items.Statuses(self._api_client)
        
    def suites(self):
        return items.Suites(self._api_client)
        
    def templates(self):
        return items.Templates(self._api_client)
        
    def tests(self):
        return items.Tests(self._api_client)
        
    def users(self):
        return items.Users(self._api_client)
        
    def variables(self):
        return items.Variables(self._api_client)
    
    
    # Utility functions
    
    def connect(self,
                password,
                base_url,
                ssl_verification_level):
        # TODO: validate url
        if self._api_client is None:
            auth = (self._user, password)
            self._api_client = TestRailAPIClient(base_url,
                                                 auth,
                                                 ssl_verification_level)

    # TODO: Do something with the response
    # TODO: Validate inputs?
