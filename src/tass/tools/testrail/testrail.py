from tass.tools.testrail.testrail_apiclient import TestRailAPIClient



def check_connection(func):
    def wrapper(api, *args):
        if api._api_client is not None:
            return func(api, *args)
        else:
            print("Not connected.")
    return wrapper


class TestRail():
    def __init__(self, user):
        self._user = user
        self._api_client = None

    # Testrail api endpoint utility functions
    # each functions returns a testrail item that manages endpoints for each type
    
    def attachments(self):
        from tass.tools.testrail.items.attachments import Attachments
        return Attachments(self._api_client)

    def bdds(self):
        from tass.tools.testrail.items.attachments import BDDs
        return BDDs(self._api_client)

    def cases(self):
        from tass.tools.testrail.items.cases import Cases
        return Cases(self._api_client)
        
    def configurations(self):
        from tass.tools.testrail.items.configurations import Configurations
        return Configurations(self._api_client)
        
    def groups(self):
        from tass.tools.testrail.items.groups import Groups
        return Groups(self._api_client)
        
    def milestones(self):
        from tass.tools.testrail.items.milestones import Milestones
        return Milestones(self._api_client)
        
    def plans(self):
        from tass.tools.testrail.items.plans import Plans
        return Plans(self._api_client)
        
    def priorities(self):
        from tass.tools.testrail.items.priorities import Priorities
        return Priorities(self._api_client)
        
    def projects(self):
        from tass.tools.testrail.items.projects import Projects
        return Projects(self._api_client)
        
    def reports(self):
        from tass.tools.testrail.items.reports import Reports
        return Reports(self._api_client)
        
    def results(self):
        from tass.tools.testrail.items.results import Results
        return Results(self._api_client)
        
    def roles(self):
        from tass.tools.testrail.items.roles import Roles
        return Roles(self._api_client)
        
    def runs(self):
        from tass.tools.testrail.items.runs import Runs
        return Runs(self._api_client)
        
    def sections(self):
        from tass.tools.testrail.items.sections import Sections
        return Sections(self._api_client)
        
    def shared_steps(self):
        from tass.tools.testrail.items.shared_steps import SharedSteps
        return SharedSteps(self._api_client)
        
    def statuses(self):
        from tass.tools.testrail.items.statuses import Statuses
        return Statuses(self._api_client)
        
    def suites(self):
        from tass.tools.testrail.items.suites import Suites
        return Suites(self._api_client)
        
    def templates(self):
        from tass.tools.testrail.items.templates import Templates
        return Templates(self._api_client)
        
    def tests(self):
        from tass.tools.testrail.items.tests import Tests
        return Tests(self._api_client)
        
    def users(self):
        from tass.tools.testrail.items.users import Users
        return Users(self._api_client)
        
    def variables(self):
        from tass.tools.testrail.items.variables import Variables
        return Variables(self._api_client)
    
    
    # Utility functions
    
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
