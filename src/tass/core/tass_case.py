from datetime import datetime
from tass.core.tass_items import TassItem
from tass.drivers.browserdriver import newDriver
from tass.actions.actions import action
from tass.exceptions.assertion_errors import TassHardAssertionError
from tass.exceptions.assertion_errors import TassSoftAssertionError


class TassCase(TassItem):
    def execute_tass(self):
        self._start_time = datetime.now().strftime("%d-%m-%Y--%H_%M_%S")
        self._status = 'incomplete'
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
                error = {
                    "status": "failed",
                    "status_message": soft_fail.message
                    }
                step.update(error)
                self._errors.append(step)
            except TassHardAssertionError as fail:
                # TODO: Error message should be attached here.
                error = {
                    "status": "failed",
                    "status_message": fail.message
                    }
                step.update(error)
                self._errors.append(step)
                break

        if (len(self._errors) > 0):
            self._status = 'failed'
        else:
            self._status = 'passed'
        self.driver.quit()

    def __init__(self, *, steps=[], browser_config={}, **kwargs):
        # TODO: Include Pages after confirming data structure
        super().__init__(**kwargs)
        self._browser_config = browser_config
        self._steps = steps
        self._driver = None
        self._start_time = 'not started'
        self._status = 'untested'
        self._errors = []

    @property
    def driver(self):
        if (self._driver is None):
            self._driver = newDriver(**self._browser_config)
        return self._driver

    @property
    def steps(self):
        return self._steps

    def toJson(self):
        return {
            "name": self.name,
            "uuid": self.uuid,
            "start_time": self._start_time,
            "status": self._status,
            "browser": self.driver,
            "errors": self._errors,
            "steps": self._steps
        }


def _execute_step(step, driver):
    raw = step.get('parameters', None)
    if (not isinstance(raw, dict)):
        params = dict(zip(it := iter(raw), it))
    else:
        params = raw
    action(*step.get('action'))(driver=driver, **params)
