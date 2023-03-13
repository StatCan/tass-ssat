import json
from tass.core.tass_items import TassFile
from tass.core.tass_case import TassCase
from tass.drivers.supportedbrowsers import Browsers


class TassSuite(TassFile):

    def collect(self):
        # TODO: Collect all test cases as TassItems and yield
        pass


class TassRun(TassFile):

    def __init__(self,  path, test_cases, browser, **kwargs):
        super().__init__(path, **kwargs)
        self._test_cases = test_cases
        self._browser_name = browser

    def collect(self):
        # TODO: Collect all test cases as TassItems,
        # then collect all TestSuites and yield TassItems
        # print(self.file)

        try:
            browser = Browsers.browser(self._browser_name)
        except (KeyError) as ke:
            print('')
            print('Not a supported browser: ', self._browser_name)
            raise ke

        for case in self._test_cases:
            driver = {'browser': browser,
                      'config': json.load(open('tass/config/browsers.json'))
                      .get(browser, {})}
            yield TassCase(parent=self, browser_config=driver, **case)
