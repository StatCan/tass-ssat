from datetime import datetime
from .tass_items import TassFile
from .tass_case import TassCase
from ..log.logging import getLogger


class TassSuite(TassFile):

    def collect(self):
        # TODO: Collect all test cases as TassItems and yield
        pass


class TassRun(TassFile):

    logger = getLogger(__name__)

    def __init__(self, path, test_cases,
                 test_suites, action_managers,
                 **kwargs):
        super().__init__(path, **kwargs)
        self._managers = action_managers
        self._raw_test_cases = test_cases
        self._raw_test_suites = test_suites
        self._start_time = 'not started'
        self._completed_cases = []
        self._has_error = False

    def __str__(self):
        str_ = f"""
                UUID: {self.uuid}
                Build: {self.build}
               """
        return str_

    @property
    def start_time(self):
        return self._start_time

    @property
    def completed_cases(self):
        return self._completed_cases

    @property
    def has_error(self):
        return self._has_error

    def record_error(self):
        self._has_error = True

    def toJson(self):
        return {
            "name": self.title,
            "uuid": self.uuid,
            "test_start": self._start_time,
            "test_cases": self._completed_cases,
            "action_managers": [v.toJson() for v in self._managers.values()]
        }

    def collect(self):
        # TODO: Collect all test cases as TassItems,
        # then collect all TestSuites and yield TassItems

        self._start_time = datetime.now().strftime("%d-%m-%Y--%H_%M_%S")
        self.logger.debug("Start time (%s): %s", self.uuid, self._start_time)
        for case in self._raw_test_cases:
            tasscase = TassCase.from_parent(parent=self, managers = self._managers, **case)

            self.logger.debug("Collected: %r", tasscase)
            yield tasscase

            self._completed_cases.append(tasscase)
            self.logger.debug("Added to completed cases: %s", tasscase.uuid)
