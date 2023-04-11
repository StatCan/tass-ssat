from tass.core.tass_items import TassItem
from tass.drivers.browserdriver import newDriver
from tass.actions.actions import action
from tass.exceptions.assertion_errors import TassAssertionError
from tass.exceptions.assertion_errors import TassSoftAssertionError


class TassCase(TassItem):
    def execute_tass(self):
        # print(self.steps)
        for step in self.steps:
            print('')
            print('* * * * * * * * * *')
            print(step)
            print('* * * * * * * * * *')

            try:
                # Executing the step, catching the custom exception
                # reporting a failed step here.
                _execute_step(step, self.driver)
                step.update({"status": "passed"})
            except TassSoftAssertionError as soft_fail:
                # TODO: Error message should be attached here.
                step.update({"status": "failed"})
            except TassAssertionError as fail:
                # TODO: Error message should be attached here.
                step.update({"status": "failed"})
                break

        self.driver.quit()

    def __init__(self, *, steps=[], browser_config={}, **kwargs):
        # TODO: Include Pages after confirming data structure
        super().__init__(**kwargs)
        self._browser_config = browser_config
        self._steps = steps
        self._driver = None

    @property
    def driver(self):
        if (self._driver is None):
            self._driver = newDriver(**self._browser_config)
        return self._driver

    @property
    def steps(self):
        return self._steps


def _execute_step(step, driver):
    params = dict(zip(it := iter(step.get('parameters', None)), it))
    action(*step.get('action'))(driver=driver, **params)
