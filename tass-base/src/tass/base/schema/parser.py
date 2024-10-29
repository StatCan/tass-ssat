from copy import deepcopy

from tass.base.exceptions.tass_errors import TassUUIDException, TassUUIDNotFound, TassAmbiguousUUID
from tass.base.log.logging import getLogger
from tass.report.registrar import ReporterRegistrar
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
        registrar = self._parse_reporters(job)

        # TODO: parse should only return runs.
        # Requires refactor of reporter implementation.
        # See https://github.com/StatCan/tass-ssat/issues/152
        return runs, registrar

    def _parse_job(self, path, job):

        meta = job.get("Meta", None)
        job_raw = job['Job']
        tassjob = TassJob(**job_raw, _meta=meta)

        for case in self._parse_cases(job["Test_cases"], job):
            tassjob.add_test_case(case)

    def _parse_cases(self, cases, job):
        for case in cases:
            try:
                browser = self._parse_browser(case['browser_uuid'], job)
                steps = self._parse_steps(case['steps'], job)
            except Tass

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

            return deepcopy(found[0])

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

    def _parse_browser(self, browser, job):
        self.log.debug("Using browsers: %s", browser)
        found =  list(filter(lambda b: b['uuid'] in browser, job["browsers"]))
        if len(found)>1:
            self.log.warning("Ambiguous browser configuration selected. Attempting to resolve.")
            if not all(step == found[0] for step in found[1:]):
                self.log.warning("Unable to resolve ambiguous uuids.")
                raise TassAmbiguousUUID(uuid)
        elif len(found) == 0:
            self.log.warning("No matching browser configuration found.")
            raise TassUUIDNotFound(uuid)

        return deepcopy(found[0])
