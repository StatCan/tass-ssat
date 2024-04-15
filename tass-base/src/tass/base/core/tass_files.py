from datetime import datetime
from .tass_items import TassFile
from .tass_case import TassCase
from ..drivers import supportedbrowsers as Browsers
from ..log.logging import getLogger


class TassSuite(TassFile):

    def collect(self):
        # TODO: Collect all test cases as TassItems and yield
        pass


class TassRun(TassFile):

    logger = getLogger(__name__)

    def __init__(self,  path, test_cases, test_suites, browser, **kwargs):
        super().__init__(path, **kwargs)
        self._raw_test_cases = test_cases
        self._raw_test_suites = test_suites
        self._browser_name = browser
        self._start_time = 'not started'
        self._completed_cases = []

    @property
    def start_time(self):
        return self._start_time

    def toJson(self):
        return {
            "name": self.title,
            "uuid": self.uuid,
            "browser": self._browser_name,
            "test_start": self._start_time,
            "test_cases": self._completed_cases
        }

    def collect(self):
        # TODO: Collect all test cases as TassItems,
        # then collect all TestSuites and yield TassItems

        try:
            browser = Browsers.browser(self._browser_name)
            self.logger.debug('Compatible browser selected (%s): %s',
                              self.uuid, browser)
        except (KeyError) as ke:
            self.logger.error("Unsupported browser selected (%s): %s",
                              self.uuid, self._browser_name)
            raise ke

        self._start_time = datetime.now().strftime("%d-%m-%Y--%H_%M_%S")
        self.logger.debug("Start time (%s): %s", self.uuid, self._start_time)

        for case in self._raw_test_cases:
            tasscase = TassCase.from_parent(parent=self,
                                            browser=browser,
                                            **case)

            self.logger.debug("Collected: %r", tasscase)
            yield tasscase

            self._completed_cases.append(tasscase)
            self.logger.debug("Added to completed cases: %s", tasscase.uuid)
