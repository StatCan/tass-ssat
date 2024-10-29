from datetime import datetime
from .tass_items import TassFile
from .tass_case import TassCase
from ..log.logging import getLogger


class TassJob(TassFile):

    logger = getLogger(__name__)

    def __init__(self, path,
                 _meta=None,
                 **kwargs):
        super().__init__(path, **kwargs)
        self._start_time = 'not started'
        self._completed_cases = []
        self._test_cases = []
        self._has_error = False
        if _meta:
            _meta.setdefault("results-path", "./results")
            _meta.setdefault("pages-path", "./pages")
        else:
            _meta = {
                "results-path": "./results",
                "pages-path": "./pages"
            }
        self._meta = _meta

    def __str__(self):
        str_ = f"""
                UUID: {self.uuid}
                Build: {self.build}
               """
        return str_

    def add_test_case(self, case):
        if isinstance(dict, case):
            _ = TassCase(**case)
        elif isinstance(TassCase, case):
            _ = case
        if _:
            self._test_cases.append(_)

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

        self._start_time = datetime.now().strftime("%d-%m-%Y--%H_%M_%S")
        self.logger.debug("Start time (%s): %s", self.uuid, self._start_time)
        for case in self._raw_test_cases:
            tasscase = TassCase.from_parent(parent=self,
                                            managers=self._managers, **case)

            self.logger.debug("Collected: %r", tasscase)
            yield tasscase

            self._completed_cases.append(tasscase)
            self.logger.debug("Added to completed cases: %s", tasscase.uuid)
