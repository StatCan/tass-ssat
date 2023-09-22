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

    # Roles
    # Reference: https://support.testrail.com/hc/en-us/articles/7077853258772-Roles

    @check_connection
    def get_roles(self):
        endpoint = "get_roles"
        self._api_client.get(endpoint)

    # Runs
    # Reference: https://support.testrail.com/hc/en-us/articles/7077874763156-Runs

    @check_connection
    def get_run(self, run_id):
        endpoint = f"get_run/{get_run}"
        self._api_client.get(endpoint)

    @check_connection
    def get_runs(self, project_id, **filters):
        endpoint = self._filtered_endpoint(f"get_runs/{project_id}", filters)
        self._api_client.get(endpoint)

    @check_connection
    def add_run(self, project_id, run):
        endpoint = f"add_run/{project_id}"
        self._api_client.post(endpoint, run)

    @check_connection
    def update_run(self, run_id, run):
        endpoint = f"update_run/{run_id}"
        self._api_client.post(endpoint, run)

    @check_connection
    def close_run(self, run_id):
        endpoint = f"close_run/{run_id}"
        self._api_client.post(endpoint, {})

    @check_connection
    def delete_run(self, run_id, soft=False):
        endpoint = f"delete_run/{run_id}"
        self._api_client.post(endpoint, {"soft": 1 if soft else 0})

    # Sections
    # Reference: https://support.testrail.com/hc/en-us/articles/7077918603412-Sections

    @check_connection
    def get_section(self, section_id):
        endpoint = f"get_section/{section_id}"
        self._api_client.get(endpoint)

    @check_connection
    def get_sections(self, project_id, suite_id=None, **filters):
        endpoint = f"get_sections/{project_id}"
        if suite_id:
            endpoint += f"&suite_id={suite_id}"
        endpoint = self._filtered_endpoint(endpoint, filters)
        self._api_client.get(endpoint)

    @check_connection
    def add_section(self, project_id, section):
        endpoint = f"add_section/{project_id}"
        self._api_client.post(endpoint, section)

    @check_connection
    def move_section(self, section_id, section):
        endpoint = f"move_section/{section_id}"
        self._api_client.post(endpoint, section)

    @check_connection
    def update_section(self, section_id, section):
        endpoint = f"update_section/{section_id}"
        self._api_client.post(endpoint, section)

    @check_connection
    def delete_section(self, section_id, soft=False):
        endpoint = f"delete_section/{section_id}"
        self._api_client.post(endpoint, {"soft": 1 if soft else 0})

    # Shared Steps
    # Reference: https://support.testrail.com/hc/en-us/articles/7077919815572-Shared-Steps

    @check_connection
    def get_shared_step(self, shared_step_id):
        endpoint = f"get_shared_step/{shared_step_id}"
        self._api_client.get(endpoint)

    @check_connection
    def get_shared_step_history(self, shared_step_id):
        endpoint = f"get_shared_step_history/{shared_step_id}"
        self._api_client.get(endpoint)

    @check_connection
    def get_shared_steps(self, project_id, **filters):
        endpoint = self._filtered_endpoint(f"get_shared_steps/{project_id}", filters)
        self._api_client.get(endpoint)

    @check_connection
    def add_shared_step(self, project_id, step):
        endpoint = f"add_shared_step/{project_id}"
        self._api_client.post(endpoint, step)

    @check_connection
    def delete_shared_step(self, shared_step_id, keep=True):
        endpoint = f"delete_sharede_step/{shared_step_id}"
        self._api_client.post(endpoint, {"keep_in_cases": 1 if keep else 0})

    # Status
    # Reference: https://support.testrail.com/hc/en-us/articles/7077935129364-Statuses

    @check_connection
    def get_case_statuses(self):
        endpoint = f"get_case_statuses"
        self._api_client.get(endpoint)

    @check_connection
    def get_statuses(self):
        endpoint = f"get_statuses"
        self._api_client.get(endpoint)

    # Suites
    # Reference: https://support.testrail.com/hc/en-us/articles/7077936624276-Suites

    @check_connection
    def get_suite(self, suite_id):
        endpoint = f"get_suite/{suite_id}"
        self._api_client.get(endpoint)

    @check_connection
    def get_suites(self, project_id):
        endpoint = f"get_suites/{project_id}"
        self._api_client.get(endpoint)

    @check_connection
    def add_suite(self, project_id, suite):
        endpoint = f"add_suite/{project_id}"
        self._api_client.post(endpoint, suite)

    @check_connection
    def update_suite(self, suite_id, suite):
        endpoint = f"update_suite/{suite_id}"
        self._api_client.post(endpoint, suite)

    @check_connection
    def delete_suite(self, suite_id, soft=False):
        endpoint = f"delete_suite/{suite_id}"
        self._api_client.post(endpoint, {"soft": 1 if soft else 0})

    # Templates
    # Reference: https://support.testrail.com/hc/en-us/articles/7077938165780-Templates

    @check_connection
    def get_templates(self, project_id):
        endpoint = f"get_templates/{project_id}"
        self._api_client.get(endpoint)

    # Tests
    # Reference: https://support.testrail.com/hc/en-us/articles/7077990441108-Tests

    @check_connection
    def get_test(self, test_id, **filters):
        endpoint = self._filtered_endpoint(f"get_test/{test_id}", filters)
        self._api_client.get(endpoint)

    @check_connection
    def get_tests(self, run_id, **filters):
        endpoint = self._filtered_endpoint(f"get_tests/{run_id}", filters)
        self._api_client.get(endpoint)

    # Users
    # Reference: https://support.testrail.com/hc/en-us/articles/7077978310292-Users

    @check_connection
    def get_user(self, user_id):
        endpoint = f"get_user/{user_id}"
        self._api_client.get(endpoint)

    @check_connection
    def get_current_user(self):
        endpoint = "get_current_user"
        self._api_client.get(endpoint)
    
    @check_connection
    def get_user_by_email(self, email):
        endpoint = f"get_user_by_email&email={email}"
        self._api_client.get(endpoint)

    @check_connection
    def get_users(self, project_id=None):
        endpoint = "get_users"
        if project_id is not None:
            endpoint += f"/{project_id}"
        self._api_client.get(endpoint)

    @check_connection
    def add_user(self, user):
        endpoint = "add_user"
        self._api_client.post(endpoint, user)

    @check_connection
    def update_user(self, user_id, user):
        endpoint = f"update_user/{user_id}"
        self._api_client.post(endpoint, user)

    # Variables
    # Reference: https://support.testrail.com/hc/en-us/articles/7077979742868-Variables

    @check_connection
    def get_variables(self, project_id):
        endpoint = f"get_variables/{project_id}"
        self._api_client.get(endpoint)

    @check_connection
    def add_variable(self, project_id, variable):
        endpoint = f"add_variable/{project_id}"
        self._api_client.post(endpoint, variable)

    @check_connection
    def update_variable(self, variable_id, variable):
        endpoint = f"update_variable/{variable_id}"
        self._api_client.post(endpoint, variable)

    @check_connection
    def delete_variable(self, variable_id):
        endpoint = f"delete_variable/{variable_id}"
        self._api_client.post(endpoint, {})
