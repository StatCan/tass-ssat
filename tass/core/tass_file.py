import pytest
import json
from tass.core.tass_item import TassItem
from tass.drivers.browserdriver import ChromeDriver


class TassConfig(pytest.File):

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)

    @property
    def name(self):
        return self._name

    @property
    def uuid(self):
        return self._uuid


class TassSuite(TassConfig):

    def collect(self):
        # TODO: Collect all test cases as TassItems and yield
        pass


class TassRun(pytest.File):

    def collect(self):
        # TODO: Collect all test cases as TassItems,
        # then collect all TestSuites and yield TassItems
        self.file = json.load(open(self.path))
        # print(self.file)
        self.testcases = self.file.get("test_cases", None)
        driver = ChromeDriver(json.load(open('tass/config/browsers.json'))
                              .get("chrome", {}))
        for case in self.testcases:
            yield TassItem.from_parent(self,
                                       name=case.get('title', "Untitled"),
                                       steps=case.get("steps", []),
                                       driver=driver)
