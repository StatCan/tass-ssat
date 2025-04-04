import configparser
from .testrail import TestRail
from ..reporter import ReporterBase


# TODO: Add support for test plans
class TestrailReporter(ReporterBase):
    def __init__(self, connection, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._testrail = self._connect(connection)
        self._config = self._load_config(config)

    def _load_config(self, config):
        conf = configparser.ConfigParser()
        defaults = {
            "DEFAULT": {
                "always-close-runs": False,
                "close-successful-runs": False
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

    def _start_plan(self, project_id, plan):
        response = self._testrail.plans().add_plan(project_id, plan)
        return response

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
