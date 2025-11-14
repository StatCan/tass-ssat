import warnings
from copy import deepcopy
from tass.core.exceptions.tass_errors import (
    TassUUIDNotFound,
    TassAmbiguousUUID)
from tass.core.log.logging import init_logger, getLogger
from ..actions.action_manager import get_manager
from ..job.tass_files import TassJob


class Parser():
    def __init__(self):
        self.log = getLogger(__name__)

    def parse(self, job):
        raise NotImplementedError("Parse is not implemented.")


@warnings.deprecated
class Tass1Parser(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, path, job):

        runs = self._parse_job(path, job)

        return runs

    def _parse_job(self, path, job):

        meta = job.get("Meta", None)
        init_logger(file_name=job["Job"]["uuid"], **job.get("Logger", {}))
        job_raw = job['Job']
        tassjob = TassJob(path, _meta=meta, **job_raw)

        for test in self._parse_tests(job["Tests"], job):
            tassjob.add_test_case(test)

        return tassjob

    def _parse_tests(self, tests, job):
        for test in tests:
            _out = {}
            _out['uuid'] = test['uuid']
            _out.update(self._parse_case(test['case'], job))
            _out.update(
                self._parse_configurations(
                    test['configurations'], job))
            _out.update(self._parse_managers(_out, job))
            yield _out

    def _parse_case(self, uuid, job):
        found = list(filter(lambda c: uuid == c['uuid'], job['Cases']))
        if len(found) > 1:
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

        return _case

    def _parse_configurations(self, config, job):
        configuration = {}

        def browser(uuid):
            _browser = self._parse_browser(uuid, job)
            configuration['driver'] = _browser
        def mobile(uuid):
            _mobile = self._parse_mobile(uuid, job)
            configuration['driver'] = _mobile

        registered_configuration_parsers = {
            "browser": browser,
            "mobile": mobile
        }
        for conf in config:
            k, v = conf['type'], conf['uuid']
            if k in registered_configuration_parsers:
                parser = registered_configuration_parsers[k]
                parser(v)

        return configuration

    def _parse_steps(self, steps, job):
        all_steps = job['Steps']
        step_config = []
        for uuid in steps:
            found = list(filter(lambda step: uuid == step['uuid'], all_steps))
            if len(found) > 1:
                self.log.warning(
                    "Ambiguous step configuration. Checking compatibility")
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
        found = list(filter(lambda b: b['uuid'] in browser, job["Browsers"]))
        if len(found) > 1:
            self.log.warning(
                "Ambiguous browser configuration. Attempting to resolve.")
            if not all(step == found[0] for step in found[1:]):
                self.log.warning("Unable to resolve ambiguous uuids.")
                raise TassAmbiguousUUID(browser)
        elif len(found) == 0:
            self.log.warning("No matching browser configuration found.")
            raise TassUUIDNotFound(browser)

        return deepcopy(found[0])


    def _parse_mobile(self, mobile, job):
        self.log.debug("Using browsers: %s", mobile)
        found = list(filter(lambda b: b['uuid'] in mobile, job["Mobiles"]))
        if len(found) > 1:
            self.log.warning(
                "Ambiguous mobile configuration. Attempting to resolve.")
            if not all(step == found[0] for step in found[1:]):
                self.log.warning("Unable to resolve ambiguous uuids.")
                raise TassAmbiguousUUID(mobile)
        elif len(found) == 0:
            self.log.warning("No matching mobile configuration found.")
            raise TassUUIDNotFound(mobile)

        return deepcopy(found[0])

    def _parse_managers(self, c, job):

        def sel_managers(_manager, _c):
            browser_configs = _c['driver']
            manager = get_manager(_manager, browser_configs)
            return manager

        def core_manager(_manager, _c):
            manager = get_manager(_manager)
            return manager

        parsers = {
            "selenium": sel_managers,
            "selwait": sel_managers,
            "selchain": sel_managers,
            "core": core_manager
        }

        steps = c['steps']
        _managers = set([step['action'][0] for step in steps])
        managers = {}
        for manager in _managers:
            if (manager in parsers
               and manager not in managers):

                m = parsers[manager](manager, c)
                managers.update(m)
        return {"managers": managers}


class Tass1_1Parser(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, path, job):

        runs = self._parse_job(path, job)

        return runs

    def _parse_job(self, path, job):

        meta = job.get("Meta", None)
        init_logger(file_name=job["Job"]["uuid"], **job.get("Logger", {}))
        job_raw = job['Job']
        tassjob = TassJob(path, _meta=meta, **job_raw)

        for test in self._parse_tests(job["Tests"], job):
            tassjob.add_test_case(test)

        return tassjob

    def _parse_tests(self, tests, job):
        for test in tests:
            _out = {}
            _out['uuid'] = test['uuid']
            _out.update(self._parse_case(test['case'], job))
            _out.update(
                self._parse_configurations(
                    test['configurations'], job))
            _out.update(self._parse_managers(_out, job))
            yield _out

    def _parse_case(self, uuid, job):
        found = list(filter(lambda c: uuid == c['uuid'], job['Cases']))
        if len(found) > 1:
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

        return _case

    def _parse_configurations(self, config, job):
        configurations = []

        def browser(uuid):
            _browser = self._parse_browser(uuid, job)
            conf = {
                "module_name": "browser",
                "browser_config": _browser
            }
            configurations.append(conf)

        def mobile(uuid):
            _mobile = self._parse_mobile(uuid, job)
            conf = {
                "module_name": "browser",
                "mobile_configs": _mobile
            }
            configurations.append(conf)

        registered_configuration_parsers = {
            "browser": browser,
            "mobile": mobile
        }

        for conf in config:
            k, v = conf['type'], conf['uuid']
            if k not in registered_configuration_parsers:
                self.log.warning(f"Unknown configuration type: {k}")
                continue
            parser = registered_configuration_parsers[k]
            parser(v)

        return {"configs": configurations}

    def _parse_steps(self, steps, job):
        all_steps = job['Steps']
        step_config = []
        for uuid in steps:
            found = list(filter(lambda step: uuid == step['uuid'], all_steps))
            if len(found) > 1:
                self.log.warning(
                    "Ambiguous step configuration. Checking compatibility")
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
        found = list(filter(lambda b: b['uuid'] in browser, job["Browsers"]))
        if len(found) > 1:
            self.log.warning(
                "Ambiguous browser configuration. Attempting to resolve.")
            if not all(step == found[0] for step in found[1:]):
                self.log.warning("Unable to resolve ambiguous uuids.")
                raise TassAmbiguousUUID(browser)
        elif len(found) == 0:
            self.log.warning("No matching browser configuration found.")
            raise TassUUIDNotFound(browser)

        return deepcopy(found[0])

    def _parse_mobile(self, mobile, job):
        self.log.debug("Using mobiles: %s", mobile)
        found = list(filter(lambda m: m['uuid'] in mobile, job["Mobiles"]))
        if len(found) > 1:
            self.log.warning(
                "Ambiguous mobiles configuration. Attempting to resolve.")
            if not all(step == found[0] for step in found[1:]):
                self.log.warning("Unable to resolve ambiguous uuids.")
                raise TassAmbiguousUUID(mobile)
        elif len(found) == 0:
            self.log.warning("No matching mobiles configuration found.")
            raise TassUUIDNotFound(mobile)

        return deepcopy(found[0])

    def _parse_managers(self, c, job):
        manager_configs = c["configs"]
        modules_added = []
        managers = {}
        for manager in manager_configs:
            if (manager["module_name"] not in modules_added):
                m = get_manager(**manager)
                managers.update(m)
                modules_added.append(manager["module_name"])
        self.log.info(f"Found managers for {c['uuid']}")
        self.log.info(managers.keys())
        return {"managers": managers}