from tass.base.log.logging import getLogger
from tass.report.registrar import ReporterRegistrar
from ..actions.action_manager import get_manager
from ..core.tass_files import TassRun


class Parser():
    def __init__(self):
        self.log = getLogger(__name__)

    def parse(self, job):
        raise NotImplementedError("Parse is not implemented.")


class Tass1Parser(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, path, job):

        runs = self._parse_runs(path, job)
        registrar = self._parse_reporters(job)

        # TODO: parse should only return runs.
        # Requires refactor of reporter implementation.
        # See https://github.com/StatCan/tass-ssat/issues/152
        return runs, registrar

    def _parse_runs(self, path, job):
        self.log.info("Parsing runs from job file")
        all_runs = job.get('Test_runs')
        ready_runs = []

        for run in all_runs:
            self.log.info("Reading run: %s - %s", run['uuid'], run['title'])
            run['test_cases'], managers = self._parse_cases(job, run)
            self.log.info("Run includes actions for: %s", managers)
            for browser in self._parse_browsers(job, run['browsers']):
                _managers = {}
                self.log.info("Creating run using browser: %s", browser)
                for _manager in managers:
                    if _manager not in _managers:
                        _managers.update(get_manager(_manager, config=browser))
                _run = TassRun(path, action_managers=_managers, **run)
                self.log.info("Run: %s ready to execute.", _run.uuid)

                ready_runs.append(_run)

        return ready_runs

    def _parse_suites(job):
        # TODO: Parse Suites.
        # https://github.com/StatCan/tass-ssat/issues/151
        pass

    def _parse_cases(self, job, run):
        cases = []
        test_cases = job.get('Test_cases', [])
        all_steps = job.get('Steps', [])
        for case_id in run.get('test_cases', []):
            steps = []
            case = next(
                filter(lambda _c: _c['uuid'] == case_id, test_cases)
                ).copy()

            for step in case.get('steps', []):
                _ = next(
                    filter(lambda _c: _c['uuid'] == step, all_steps)
                    ).copy()
                self.log.debug(">>>>> Reading case: %s", _)
                steps.append(_)

            case['steps'] = steps

            managers = set([_m['action'][0].lower() for _m in steps])

            cases.append(case)

        return cases, managers

    def _parse_reporters(self, job):
        reporters = job['Reporters']
        if not reporters:
            return None
        registrar = ReporterRegistrar()

        for reporter in reporters:
            self.log.debug("Registering reporter: %s -- type: %s",
                           reporter['uuid'], reporter['type'])
            registrar.register_reporter(**reporter)

        return registrar

    def _parse_browsers(self, job, browser_list):
        browsers = job['Browsers']
        self.log.debug("Using browsers: %s", browser_list)
        return filter(lambda b: b['uuid'] in browser_list, browsers)
