from datetime import datetime
from tass.core.tass_items import TassFile
from tass.core.tass_case import TassCase
import tass.drivers.supportedbrowsers as Browsers


class TassSuite(TassFile):

    def collect(self):
        # TODO: Collect all test cases as TassItems and yield
        pass


class TassRun(TassFile):

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
        self._start_time = datetime.now().strftime("%d-%m-%Y--%H_%M_%S")
        try:
            browser = Browsers.browser(self._browser_name)
        except (KeyError) as ke:
            print('')
            print('Not a supported browser: ', self._browser_name)
            raise ke

        for case in self._raw_test_cases:
            tasscase = TassCase.from_parent(parent=self,
                                            browser=browser,
                                            **case)
            yield tasscase
            self._completed_cases.append(tasscase)
