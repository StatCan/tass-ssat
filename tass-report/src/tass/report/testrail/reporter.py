from .testrail import TestRail
from ..reporter import ReporterBase


# TODO: Add support for test plans
class TestRailReporter(ReporterBase):
    def __init__(self, connection, config):
        super().__init__()
        self._testrail = self._connect(connection)
        # TODO: load configuration
        self._config = config

    def _connect(self, connection):
        tr = TestRail(connection['user'])
        ssl = connection.get('ssl-verify', 1)
        tr.connect(connection['password'],
                   connection['url-base'],
                   ssl_verification_level=ssl)
        return tr
        
    def _map(self, map, value):
        """
        Utility method to map testrail keys to 
        keys used by the tool accessing testrail.
        """
        mapping = self._config['mappings']
        m = mapping.get(map, {}).get(value, None)
        return m

    # TODO: Include logic to switch to different Testrail modes
    # ex: single suite, multiple suite.

    def start_report(self, project_id, run, *args, **kwargs):
        return self._start_run(project_id, run)
        
    def report(self, reportable, report_all=True, *args, **kwargs):
        if report_all:
            return self._add_results(reportable)
        else:
            return self._add_result(reportable)

    def end_report(self, run_id, *args, **kwargs):
        return self._close_run(run_id)
        
    def _start_run(self, project_id, run):
        response = self._testrail.runs().add_run(project_id, run)
        return response
        # TODO: examine response for status etc.
        
    def _add_results(self, run_result):
        resonse = self._testrail.results().add_results_for_cases(**run_result)
        # TODO: examine response for status etc.
        
    def _add_result(self, case_result):
        response = self._testrail.results().add_result_for_case(**case_result)
        # TODO: examine response for status etc.

    def _close_run(self, run_id):
        response = self._testrail.runs().close_run(run_id)
        # TODO: examine response for status etc.
        

    ''' 
    TODO:
    A (here)-- > Responsible for converting to testrail format using config template.

    B (tass-base)-- > Implement TASS specific behaviour

    1. Need Project id, check if numeric
        a) If given name, filter and get ID
        b) If given ID use directly.
    2. Convert TASS run to Testrail run using config
        i) Assume single suite mode
        ii) Get the testrail id for each case, filter on uuid.
    3. Add Testrail run with API
    4. Update run with results of cases.
    ''' 
        
