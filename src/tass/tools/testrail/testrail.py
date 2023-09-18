from tass.tools.testrail.testrail_apiclient import TestRailAPIClient

class TestRail():
    def __init__(self, user):
        self._user = user
        self._api_client = None
    
    def connect(self,
                pswd,
                base_url,
                ssl_verification_level=1):
        # TODO: validate url
        auth = (self._user, pswd)
        self._api_client = TestRailAPIClient(base_url,
                                             auth,
                                             ssl_verification_level)

    def is_connected(self):
        return self._api_client is not None

    def _filtered_endpoint(self, endpoint, filters):
        _endpoint = endpoint
        for param, value in filters.items():
            _endpoint += f"&{param}={value}"
        return _endpoint


    # TODO: Do something with the response
    # TODO: Validate inputs?

    # Attachments
    # Reference: https://support.testrail.com/hc/en-us/articles/7077196481428-Attachments

    def add_attachment_to_case(self, case_id, attachment):
        endpoint = f"add_attachment_to_case/{case_id}"
        self._api_client.post_attachment(endpoint, attachment)
    
    def add_attachment_to_plan(self, plan_id, attachment):
        endpoint = f"add_attachment_to_plan/{plan_id}"
        self._api_client.post_attachment(endpoint, attachment)

    def add_attachment_to_plan_entry(self, plan_id, entry_id, attachment):
        endpoint = f"add_attachment_to_plan_entry/{plan_id}/{entry_id}"
        self._api_client.post_attachment(endpoint, attachment)

    def add_attachment_to_result(self, result_id, attachment):
        endpoint = f"add_attachment_to_result/{result_id}"
        self._api_client.post_attachment(endpoint, attachment)
    
    def add_attachment_to_run(self, run_id, attachment):
        endpoint = f"add_attachment_to_run/{run_id}"
        self._api_client.post_attachment(endpoint, attachment)

    def get_attachments_for_case(self, case_id, **filters):
        endpoint = self._filtered_endpoint(f"get_attachments_for_case/{case_id}", filters)
        
        self._api_client.get(endpoint)

    def get_attachments_for_plan(self, plan_id, **filters):
        endpoint = self._filtered_endpoint(f"get_attachments_for_plan/{plan_id}", filters)
        self._api_client.get(endpoint)

    def get_attachments_for_plan_entry(self, plan_id, entry_id, **filters):
        endpoint = self._filtered_endpoint(f"get_attachments_for_plan_entry/{plan_id}/{entry_id}", filters)
        self._api_client.get(endpoint)
    
    def get_attachments_for_run(self, run_id, **filters):
        endpoint = self._filtered_endpoint(f"get_attachments_for_run/{run_id}", filters)
        self._api_client.get(endpoint)
    
    def get_attachments_for_test(self, test_id, **filters):
        endpoint = self._filtered_endpoint(f"get_attachments_for_test/{test_id}", filters)
        self._api_client.get(endpoint)

    def get_attachment(self, attachment_id):
        endpoint = f"get_attachment/{attachment_id}"
        self._api_client.get(endpoint)

    def delete_attachment(self, attachment_id):
        endpoint = f"delete_attachment/{attachment_id}"
        self._api_client.post(endpoint, None)

    # BDDs
    # Reference: https://support.testrail.com/hc/en-us/articles/7832161593620-BDDs

    def get_bdd(self, case_id):
        endpoint = f"get_bdd/{case_id}"
        self._api_client.get(endpoint)

    def add_bdd(self, section_id, bdd):
        endpoint = f"add_bdd/{section_id}"
        self._api_client.post(endpoint, bdd)

    # Cases
    # Reference: https://support.testrail.com/hc/en-us/articles/7077292642580-Cases

    def get_case(self, case_id):
        endpoint = f"get_case/{case_id}"
        self._api_client.get(endpoint)

    def get_cases(self, project_id, suite_id=None, **filters):
        endpoint = f"get_cases/{project_id}"
        if suite_id:
            endpoint += f"&suite_id={suite_id}"
        endpoint = self._filtered_endpoint(endpoint, filters)
        self._api_client.get(endpoint)

    def get_history_for_case(self, case_id, **filters):
        endpoint = self._filtered_endpoint(f"get_history_for_case/{case_id}", filters)
        self._api_client.get(endpoint)
    
    def add_case(self, section_id, case):
        endpoint = f"add_case/{section_id}"
        self._api_client.post(endpoint, case)
    
    def copy_cases_to_section(self, section_id, cases):
        endpoint = f"copy_cases_to_section/{section_id}"
        self._api_client.post(endpoint, cases)

    def update_case(self, case_id, case):
        endpoint = f"update_case/{case_id}"
        self._api_client.post(endpoint, case)

    def update_cases(self, suite_id, cases):
        endpoint = f"update_cases/{suite_id}"
        self._api_client.post(endpoint, cases)

    def move_cases_to_section(self, section_id, cases):
        endpoint = f"move_cases_to_section/{section_id}"
        self._api_client.post(endpoint, cases)

    def delete_case(self, case_id, soft=False):
        endpoint = f"delete_case/{case_id}"
        self._api_client.post(endpoint, {"soft": 1 if soft else 0})

    def delete_cases(self, suite_id, cases, soft=False):
        endpoint = f"delete_cases/{suite_id}"
        _delete = {"case_ids": cases, "soft":1 if soft else 0}
        self._api_client.post(endpoint, _delete)

    # Case Fields
    # Reference: https://support.testrail.com/hc/en-us/articles/7077281158164-Case-Fields

    def get_case_fields(self):
        endpoint = "get_case_fields"
        self._api_client.get(endpoint)

    def add_case_field(self, field):
        endpoint = "add_case_field"
        self._api_client.post(endpoint, field)

    # Case Types
    # Reference: https://support.testrail.com/hc/en-us/articles/7077295487252-Case-Types

    def get_case_types(self):
        endpoint = "get_case_types"
        self._api_client.get(endpoint)

    # Configurations
    # Reference: https://support.testrail.com/hc/en-us/articles/7077298488340-Configurations

    def get_configs(self, project_id):
        endpoint = f"get_configs/{project_id}"
        self._api_client.get(endpoint)

    def add_config_group(self, project_id, name):
        endpoint = f"add_config_group/{project_id}"
        self._api_client.post(endpoint, {"name": name})

    def add_config(self, config_group_id, name):
        endpoint = f"add_config/{config_group_id}"
        self._api_client.post(endpoint, {"name": name})

    def update_config_group(self, config_group_id, name):
        endpoint = f"update_config_group/{config_group_id}"
        self._api_client.post(endpoint, {"name": name})

    def update_config(self, config_id, name):
        endpoint = f"update_config/{config_id}"
        self._api_client.post(endpoint, {"name": name})

    def delete_config_group(self, config_group_id):
        endpoint = f"delete_config_group/{config_group_id}"
        self._api_client.post(endpoint, {})

    def delete_config(self, config_id):
        endpoint = f"delete_config/{config_id}"
        self._api_client.post(endpoint, {})

    # Datasets
    # Reference: https://support.testrail.com/hc/en-us/articles/7077300491540-Datasets

    def get_dataset(self, dataset_id):
        endpoint = f"get_dataset/{dataset_id}"
        self._api_client.get(endpoint)

    def get_datasets(self, project_id):
        endpoint = f"get_datasets/{project_id}"
        self._api_client.get(endpoint)

    def add_dataset(self, project_id, dataset):
        endpoint = f"add_dataset/{project_id}"
        self._api_client.post(endpoint, dataset)

    def update_dataset(self, dataset_id, dataset):
        endpoint = f"update_dataset/{dataset_id}"
        self._api_client.post(endpoint, dataset)

    def delete_dataset(self, dataset_id):
        endpoint = f"delete_dataset/{dataset_id}"
        self._api_client.post(endpoint, {})

    # Groups
    # References: https://support.testrail.com/hc/en-us/articles/7077338821012-Groups

    def get_group(self, group_id):
        endpoint = f"get_group/{group_id}"
        self._api_client.get(endpoint)

    def get_groups(self):
        endpoint = "get_groups"
        self._api_client.get(endpoint)

    def add_group(self, group):
        endpoint = "add_group"
        self._api_client.post(endpoint, group)

    def update_group(self, group_id, group):
        endpoint = f"update_group/{group_id}"
        self._api_client.post(endpoint, group)

    def delete_group(self, group_id):
        endpoint = f"delete_group/{group_id}"
        self._api_client.post(endpoint, {})

    # Milestones
    # References: https://support.testrail.com/hc/en-us/articles/7077723976084-Milestones

    def get_milestone(self, milestone_id):
        endpoint = f"get_milestone/{milestone_id}"
        self._api_client.get(endpoint)
    
    def get_milestones(self, project_id, **filters):
        endpoint = self._filtered_endpoint(f"get_milestones/{project_id}", filters)
        self._api_client.get(endpoint)
    
    def add_milestone(self, project_id, milestone):
        endpoint = f"add_milestone/{project_id}"
        self._api_client.post(endpoint, milestone)

    def update_milesonte(self, milestone_id, milestone):
        endpoint = f"update_milestone/{milestone_id}"
        self._api_client.post(endpoint, milestone)
    
    def delete_milestone(self, milestone_id):
        endpoint = f"delete_milestone/{milestone_id}"
        self._api_client.post(endpoint, {})

    # Plans
    # Reference: https://support.testrail.com/hc/en-us/articles/7077711537684-Plans

    def get_plan(self, plan_id):
        endpoint = f"get_plan/{plan_id}"
        self._api_client.get(endpoint)

    def get_plans(self, project_id, **filters):
        endpoint = self._filtered_endpoint(f"get_plans/{project_id}", filters)
        self._api_client.get(endpoint)

    def add_plan(self, project_id, plan):
        endpoint = f"add_plan/{project_id}"
        self._api_client.post(endpoint, plan)

    def add_plan_entry(self, plan_id, entry):
        endpoint = f"add_plan_entry/{plan_id}"
        self._api_client.post(endpoint, entry)

    def add_run_to_plan_entry(self, plan_id, entry_id, run):
        endpoint = f"add_plan_to_plan_entry/{plan_id}/{entry_id}"
        self._api_client.post(endpoint, run)

    def update_plan(self, project_id, plan):
        endpoint = f"update_plan/{project_id}"
        self._api_client.post(endpoint, plan)

    def update_plan_entry(self, plan_id, entry):
        endpoint = f"update_plan_entry/{plan_id}"
        self._api_client.post(endpoint, entry)

    def update_run_in_plan_entry(self, plan_id, entry_id, run):
        endpoint = f"update_run_in_plan_entry/{plan_id}/{entry_id}"
        self._api_client.post(endpoint, run)

    def close_plan(self, plan_id):
        endpoint = f"close_plan/{plan_id}"
        self._api_client.post(endpoint, {})

    def delete_plan(self, plan_id):
        endpoint = f"delete_plan/{plan_id}"
        self._api_client.post(endpoint, {})

    def delete_plan_entry(self, plan_id, entry_id):
        endpoint = f"delete_plan_entry/{plan_id}/{entry_id}"
        self._api_client.post(endpoint, {})

    def delete_run_from_plan_entry(self, run_id):
        endpoint = f"delete_run_from_plan_entry/{run_id}"
        self._api_client.post(endpoint, {})

    # Priorities
    # Reference: https://support.testrail.com/hc/en-us/articles/7077746564244-Priorities

    def get_priorities(self):
        endpoint = "get_priorities"
        self._api_client.get(endpoint)

    # Projects
    # Reference: https://support.testrail.com/hc/en-us/articles/7077792415124-Projects

    def get_project(self, project_id):
        endpoint = f"get_project/{project_id}"
        self._api_client.get(endpoint)

    def get_projects(self, **filters):
        endpoint = self._filtered_endpoint("get_projects", filters)
        self._api_client.get(endpoint)

    def add_project(self, project):
        endpoint = "add_project"
        self._api_client.post(endpoint, project)

    def update_project(self, project_id, project):
        endpoint = f"update_project/{project_id}"
        self._api_client.post(endpoint, project)

    def delete_project(self, project_id):
        endpoint = f"delete_project/{project_id}"
        self._api_client.post(endpoint, {})

    # Reports
    # Reference: https://support.testrail.com/hc/en-us/articles/7077825062036-Reports

    def get_reports(self, project_id):
        endpoint = f"get_reports/{project_id}"
        self._api_client.get(endpoint)

    def run_report(self, report_template_id):
        endpoint = f"run_report/{report_template_id}"
        self._api_client.get(endpoint)

    # Results
    # Reference: https://support.testrail.com/hc/en-us/articles/7077819312404-Results

    def get_results(self, test_id, **filters):
        endpoint = self._filtered_endpoint(f"get_results/{test_id}", filters)
        self._api_client.get(endpoint)

    def get_results_for_case(self, run_id, case_id, **filters):
        endpoint = self._filtered_endpoint(f"get_results_for_case/{run_id}/{case_id}", filters)
        self._api_client().get(endpoint)

    def get_results_for_run(self, run_id, **filters):
        endpoint = self._filtered_endpoint(f"get_results_for_run/{case_id}", filters)
        self._api_client().get(endpoint)

    def add_result(self, test_id, result):
        endpoint = f"add_result/{test_id}"
        self._api_client.post(endpoint, result)

    def add_result_for_case(self, run_id, case_id, result):
        endpoint = f"add_result_for_case/{run_id}/{case_id}"
        self._api_client.post(endpoint, result)

    def add_results(self, run_id, results):
        endpoint = f"add_results/{run_id}"
        self._api_client.post(endpoint, results)

    def add_results_for_cases(self, run_id, results):
        endpoint = f"add_results_for_cases/{run_id}"
        self._api_client.post(endpoint, results)

    # Result Fields
    # Reference: https://support.testrail.com/hc/en-us/articles/7077871398036-Result-Fields

    def get_result_fields(self):
        endpoint = "get_result_fields"
        self._api_client.get(endpoint)

    # Roles
    # Reference: https://support.testrail.com/hc/en-us/articles/7077853258772-Roles

    def get_roles(self):
        endpoint = "get_roles"
        self._api_client.get(endpoint)

    # Runs
    # Reference: https://support.testrail.com/hc/en-us/articles/7077874763156-Runs

    def get_run(self, run_id):
        endpoint = f"get_run/{get_run}"
        self._api_client.get(endpoint)

    def get_runs(self, project_id, **filters):
        endpoint = self._filtered_endpoint(f"get_runs/{project_id}", filters)
        self._api_client.get(endpoint)

    def add_run(self, project_id, run):
        endpoint = f"add_run/{project_id}"
        self._api_client.post(endpoint, run)

    def update_run(self, run_id, run):
        endpoint = f"update_run/{run_id}"
        self._api_client.post(endpoint, run)

    def close_run(self, run_id):
        endpoint = f"close_run/{run_id}"
        self._api_client.post(endpoint, {})

    def delete_run(self, run_id, soft=False):
        endpoint = f"delete_run/{run_id}"
        self._api_client.post(endpoint, {"soft": 1 if soft else 0})

    # Sections
    # Reference: https://support.testrail.com/hc/en-us/articles/7077918603412-Sections

    def get_section(self, section_id):
        endpoint = f"get_section/{section_id}"
        self._api_client.get(endpoint)

    def get_sections(self, project_id, suite_id=None, **filters):
        endpoint = f"get_sections/{project_id}"
        if suite_id:
            endpoint += f"&suite_id={suite_id}"
        endpoint = self._filtered_endpoint(endpoint, filters)
        self._api_client.get(endpoint)

    def add_section(self, project_id, section):
        endpoint = f"add_section/{project_id}"
        self._api_client.post(endpoint, section)

    def move_section(self, section_id, section):
        endpoint = f"move_section/{section_id}"
        self._api_client.post(endpoint, section)

    def update_section(self, section_id, section):
        endpoint = f"update_section/{section_id}"
        self._api_client.post(endpoint, section)

    def delete_section(self, section_id, soft=False):
        endpoint = f"delete_section/{section_id}"
        self._api_client.post(endpoint, {"soft": 1 if soft else 0})

    # Shared Steps
    # Reference: https://support.testrail.com/hc/en-us/articles/7077919815572-Shared-Steps

    def get_shared_step(self, shared_step_id):
        endpoint = f"get_shared_step/{shared_step_id}"
        self._api_client.get(endpoint)

    def get_shared_step_history(self, shared_step_id):
        endpoint = f"get_shared_step_history/{shared_step_id}"
        self._api_client.get(endpoint)

    def get_shared_steps(self, project_id, **filters):
        endpoint = self._filtered_endpoint(f"get_shared_steps/{project_id}", filters)
        self._api_client.get(endpoint)

    def add_shared_step(self, project_id, step):
        endpoint = f"add_shared_step/{project_id}"
        self._api_client.post(endpoint, step)

    def delete_shared_step(self, shared_step_id, keep=True):
        endpoint = f"delete_sharede_step/{shared_step_id}"
        self._api_client.post(endpoint, {"keep_in_cases": 1 if keep else 0})

    # Status
    # Reference: https://support.testrail.com/hc/en-us/articles/7077935129364-Statuses

    def get_case_statuses(self):
        endpoint = f"get_case_statuses"
        self._api_client.get(endpoint)

    def get_statuses(self):
        endpoint = f"get_statuses"
        self._api_client.get(endpoint)

    # Suites
    # Reference: https://support.testrail.com/hc/en-us/articles/7077936624276-Suites

    def get_suite(self, suite_id):
        endpoint = f"get_suite/{suite_id}"
        self._api_client.get(endpoint)

    def get_suites(self, project_id):
        endpoint = f"get_suites/{project_id}"
        self._api_client.get(endpoint)

    def add_suite(self, project_id, suite):
        endpoint = f"add_suite/{project_id}"
        self._api_client.post(endpoint, suite)

    def update_suite(self, suite_id, suite):
        endpoint = f"update_suite/{suite_id}"
        self._api_client.post(endpoint, suite)

    def delete_suite(self, suite_id, soft=False):
        endpoint = f"delete_suite/{suite_id}"
        self._api_client.post(endpoint, {"soft": 1 if soft else 0})

    # Templates
    # Reference: https://support.testrail.com/hc/en-us/articles/7077938165780-Templates

    def get_templates(self, project_id):
        endpoint = f"get_templates/{project_id}"
        self._api_client.get(endpoint)

    # Tests
    # Reference: https://support.testrail.com/hc/en-us/articles/7077990441108-Tests

    def get_test(self, test_id, **filters):
        endpoint = self._filtered_endpoint(f"get_test/{test_id}", filters)
        self._api_client.get(endpoint)

    def get_tests(self, run_id, **filters):
        endpoint = self._filtered_endpoint(f"get_tests/{run_id}", filters)
        self._api_client.get(endpoint)

    # Users
    # Reference: https://support.testrail.com/hc/en-us/articles/7077978310292-Users

    def get_user(self, user_id):
        endpoint = f"get_user/{user_id}"
        self._api_client.get(endpoint)

    def get_current_user(self):
        endpoint = "get_current_user"
        self._api_client.get(endpoint)
    
    def get_user_by_email(self, email):
        endpoint = f"get_user_by_email&email={email}"
        self._api_client.get(endpoint)

    def get_users(self, project_id=None):
        endpoint = "get_users"
        if project_id is not None:
            endpoint += f"/{project_id}"
        self._api_client.get(endpoint)

    def add_user(self, user):
        endpoint = "add_user"
        self._api_client.post(endpoint, user)

    def update_user(self, user_id, user):
        endpoint = f"update_user/{user_id}"
        self._api_client.post(endpoint, user)

    # Variables
    # Reference: https://support.testrail.com/hc/en-us/articles/7077979742868-Variables

    def get_variables(self, project_id):
        endpoint = f"get_variables/{project_id}"
        self._api_client.get(endpoint)

    def add_variable(self, project_id, variable):
        endpoint = f"add_variable/{project_id}"
        self._api_client.post(endpoint, variable)

    def update_variable(self, variable_id, variable):
        endpoint = f"update_variable/{variable_id}"
        self._api_client.post(endpoint, variable)

    def delete_variable(self, variable_id):
        endpoint = f"delete_variable/{variable_id}"
        self._api_client.post(endpoint, {})
