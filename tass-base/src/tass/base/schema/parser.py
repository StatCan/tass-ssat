from copy import deepcopy

from tass.base.exceptions.tass_errors import TassUUIDException, TassUUIDNotFound, TassAmbiguousUUID
from tass.base.log.logging import getLogger
from tass.report.registrar import ReporterRegistrar
from ..actions.action_manager import get_manager
from ..core.tass_files import TassJob
from ..core.tass_case import TassCase


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
        return runs

    def _parse_job(self, path, job):

        meta = job.get("Meta", None)
        job_raw = job['Job']
        tassjob = TassJob(path, _meta=meta, **job_raw)

        for case in self._parse_cases(job["Test_cases"], job):
            tassjob.add_test_case(case)

        return tassjob

    def _parse_cases(self, cases, jobfile, ):
        for case in cases:
            try:
                if 'browser' in case:
                    self.log.debug("Trying to load browser configurations.")
                    _browser = self._parse_browser(case['browser'], jobfile)

                steps = self._parse_steps(case['steps'], jobfile)
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
