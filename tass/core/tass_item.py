import pytest
import tass.actions.selenium as actions


class TassItem(pytest.Function):
    def tass_test(self):
        # print(self.steps)
        for step in self.steps:
            print('')
            print('* * * * * * * * * *')
            print(step)
            print('* * * * * * * * * *')
            _execute_step(step, self.driver)

    def __init__(self, *, browser_config, steps, **kwargs):
        # TODO: Include Pages after confirming data structure for both
        super().__init__(callobj=self.tass_test, **kwargs)
        self.browser_config = browser_config
        self.steps = steps


def _execute_step(step, driver):
    params = dict(zip(it := iter(step.get('parameters', None)), it))
    getattr(actions, step.get('action'))(driver=driver, **params)
