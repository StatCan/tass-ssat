import pytest


class TassConfig(pytest.File):

    def __init__(self, uuid, **kwargs):
        super().__init__(self, **kwargs)
        self._uuid = uuid

    @property
    def name(self):
        return self._name

    @property
    def uuid(self):
        return self._uuid


class TassSuite(TassConfig):

    def __init__(self, *,
                 testcases,
                 **kwargs):
        super().__init__(self, **kwargs)
        self.testcases = testcases
        
    def collect(self):
        # TODO: Collect all test cases as TassItems and yield
        pass
        
    # TODO: implement custom from_parent


class TassRun(TassConfig):
    
    def __init__(self, *,
                 testcases,
                 testsuites,
                 **kwargs):

    def collect(self):
        # TODO: Collect all test cases as TassItems, then collect all TestSuites and yield TassItems
        pass
        
    # TODO: implement custom from_parent