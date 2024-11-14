import configparser
from .testrail import TestRail
from ..core.reporter import ReporterBase


# TODO: Add support for test plans
class TestrailReporter(ReporterBase):
    def __init__(self, connection, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._testrail = self._connect(connection)
        # TODO: load configuration
        self._config = self._load_config(config)

    def _load_config(self, config):
        conf = configparser.ConfigParser()
        defaults = {
            "DEFAULT": {
                "always-close-runs": False,
                "close-succesful-runs": False
            }
        }

        # Load defaults first.
        conf.read_dict(defaults)

        # Load configs
        tr = {"testrail": config}
        conf.read_dict(tr)
        return conf

    @property
    def config(self):
        return self._config

    def _connect(self, connection):
        tr = TestRail(connection['user'])
        ssl = connection.get('ssl-verify', 1)
        tr.connect(connection['password'],
                   connection['url-base'],
                   ssl_verification_level=ssl)
        return tr

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
        response = self._testrail.results().add_results_for_cases(**run_result)
        return response
        # TODO: examine response for status etc.

    def _add_result(self, case_result):
        response = self._testrail.results().add_result_for_case(**case_result)
        return response
        # TODO: examine response for status etc.

    def _close_run(self, run_id):
        response = self._testrail.runs().close_run(run_id)
        return response
        # TODO: examine response for status etc.

    '''
    TODO:
    A (here)-- > Responsible for converting
                 to testrail format using config template.

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
