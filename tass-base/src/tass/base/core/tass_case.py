from datetime import datetime
from .tass_items import TassItem
from ..actions.action_manager import get_manager
from ..exceptions.assertion_errors import TassHardAssertionError
from ..exceptions.assertion_errors import TassSoftAssertionError


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
                _execute_step(step, self._managers)
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

    def __init__(self, *, steps=[], browser, **kwargs):
        # TODO: Include Pages after confirming data structure
        super().__init__(**kwargs)
        self._browser = browser
        self._steps = steps
        self._start_time = 'not started'
        self._status = 'untested'
        self._errors = []
        self._managers = {}

        self._init_managers('selenium', 'selenium',
                            browser=self._browser,
                            config=self._config)
        self._init_managers('selwait',
                            self._managers['selenium'].wait_manager())
        self._init_managers('core', 'core')

    def _init_managers(self, key, manager, **kwargs):
        if (isinstance(manager, str)):
            self._managers[key] = get_manager(manager, **kwargs)
        else:
            self._managers[key] = manager

    def _quit_managers(self):
        for manager in self._managers.values():
            try:
                manager.quit()
            except NotImplementedError:
                print('Manager does not have quit function')

    @property
    def steps(self):
        return self._steps

    def toJson(self):
        return {
            "name": self.title,
            "uuid": self.uuid,
            "start_time": self._start_time,
            "status": self._status,
            "errors": self._errors,
            "steps": self._steps
        }


def _execute_step(step, managers):
    raw = step.get('parameters', None)
    if (not isinstance(raw, dict)):
        params = dict(zip(it := iter(raw), it))
    else:
        params = raw
    action = step.get('action')
    if (action[0] in managers):
        managers[action[0]].action(action[1], **params)
