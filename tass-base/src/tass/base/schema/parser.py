from copy import deepcopy
from tass.base.exceptions.tass_errors import TassUUIDException, TassUUIDNotFound, TassAmbiguousUUID
from tass.base.log.logging import getLogger
from ..actions.action_manager import get_manager
from ..core.tass_files import TassJob


class Parser():
    def __init__(self):
        self.log = getLogger(__name__)

    def parse(self, job):
        raise NotImplementedError("Parse is not implemented.")


class Tass1Parser(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, path, job):

        runs = self._parse_job(path, job)

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
        managers = set()
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
            managers.update([_m['action'][0].lower() for _m in steps])

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
        return runs

    def _parse_job(self, path, job):

        meta = job.get("Meta", None)
        job_raw = job['Job']
        tassjob = TassJob(path, _meta=meta, **job_raw)

        for test in self._parse_tests(job["Test"], job):
            tassjob.add_test_case(test)

        return tassjob

    def _parse_tests(self, tests, job):
        for test in tests:
            _out = {}
            _out['uuid'] = test['uuid']
            _out.update(self._parse_case(test['case'], job))
            _out.update(self._parse_configurations(test['configurations']))
        pass

    def _parse_case(self, uuid, job):
        found = list(filter(lambda c: uuid == c['uuid'], job['Cases']))
        if len(found)>1:
            self.log.warning("Ambiguous case selected. Checking compatibility")
            if not all(c == found[0] for c in found[1:]):
                self.log.warning("Unable to resolve ambiguous uuids.")
                raise TassAmbiguousUUID(uuid)
            else:
                self.log.warning("Ambigous case conflict resolved.")
        elif len(found) == 0:
            self.log.warning("No matching case found.")
            raise TassUUIDNotFound(uuid)

        _case = deepcopy(found[0])
        _case['steps'] = self._parse_steps(found[0]['steps'], job)

        _case.update(self._parse_configurations())

        m = set([step['action'][0] for step in _case['steps']])



    def _parse_configurations(self, config, job):
        configuration = {}
        def browser(uuid):
            _browser = self._parse_browser(uuid, job)
            configuration['browser'] = _browser

        registered_configuration_parsers = {
            "browser": browser
        }

        for conf in config:
            k, v = conf['type'], conf['uuid']
            if k in registered_configuration_parsers:
                parser = registered_configuration_parsers[k]
                parser(v)

        return configuration


    def _parse_cases(self, cases, job):
        for case in cases:
            try:
                if 'browser' in case:
                    self.log.debug("Trying to load browser configurations.")
                    _browser = self._parse_browser(case['browser'], job)

                steps = self._parse_steps(case['steps'], job)
                m = set([x['action'][0] for x in steps])

                case['steps'] = steps
                case['managers'] = {}
                for manager in m:
                    case['managers'].update(get_manager(manager, browser_config=_browser))


            except TassUUIDException as e:
                self.log.warning(e)
                continue

            yield case

    def _parse_steps(self, steps, job):
        all_steps = job['Steps']
        step_config = []
        for uuid in steps:
            found = list(filter(lambda step: uuid == step['uuid'], all_steps))
            if len(found)>1:
                self.log.warning("Ambiguous step configuration selected. Checking compatibility")
                if not all(step == found[0] for step in found[1:]):
                    self.log.warning("Unable to resolve ambiguous uuids.")
                    raise TassAmbiguousUUID(uuid)
            elif len(found) == 0:
                self.log.warning("No matching step configuration found.")
                raise TassUUIDNotFound(uuid)

            step_config.append(deepcopy(found[0]))
        return step_config

    def _parse_browser(self, browser, job):
        self.log.debug("Using browsers: %s", browser)
        found =  list(filter(lambda b: b['uuid'] in browser, job["Browsers"]))
        if len(found)>1:
            self.log.warning("Ambiguous browser configuration selected. Attempting to resolve.")
            if not all(step == found[0] for step in found[1:]):
                self.log.warning("Unable to resolve ambiguous uuids.")
                raise TassAmbiguousUUID(browser)
        elif len(found) == 0:
            self.log.warning("No matching browser configuration found.")
            raise TassUUIDNotFound(browser)

        return deepcopy(found[0])
