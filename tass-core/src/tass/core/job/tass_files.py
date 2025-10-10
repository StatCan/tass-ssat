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
        self._status = "untested"
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
        if isinstance(case, dict):
            _ = TassCase.from_parent(parent=self, **case)
        elif isinstance(case, TassCase):
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
            "parent": self.parent,
            "status": self._status,
            "test_start": self._start_time,
            "test_cases": [c.toJson() for c in self._completed_cases]
        }

    def collect(self):
        self._start_time = datetime.now().strftime("%d-%m-%Y--%H_%M_%S")
        self.logger.debug("Start time (%s): %s", self.uuid, self._start_time)
        self._status = "incomplete"
        for case in self._test_cases:

            self.logger.debug("Collected: %r", case)
            yield case

            self._completed_cases.append(case)
            self.logger.debug("Added to completed cases: %s", case.uuid)
        if self.has_error:
            self._status = "failed"
        else:
            self._status = "passed"
