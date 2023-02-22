import pytest
import tass.actions.selenium as actions


class TassItem(pytest.Item):

    def __init__(self, *, driver, steps, **kwargs):
        # TODO: Include Pages after confirming data structure for both
        super().__init__(**kwargs)
        self.driver = driver
        self.steps = steps

    def runtest(self):
        # TODO: Execute test steps from job/config file
        print(self.steps)
        for step in self.steps:
            print('* * * * * * * * * *')
            print(step)
            print('* * * * * * * * * *')
            _execute_step(step, self.driver)

        self.driver.quit()


def _execute_step(step, driver):
    params = dict(zip(it := iter(step.get('parameters', None)), it))
    getattr(actions, step.get('action'))(driver=driver, **params)
