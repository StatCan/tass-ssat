import pytest

class TassItem(pytest.Item):

    def __init__(self, *, driver, steps, **kwargs):
        # TODO: Include Pages and Steps after confirming data structure for both
        super().__init__(**kwargs)
        self.driver = driver
        self.steps = steps
        
    def runtest(self):
        # TODO: Execute test steps from job/config file
        
    # TODO: implement custom from_parent
        