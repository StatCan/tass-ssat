from datetime import datetime
from copy import deepcopy
from .tass_items import TassItem
from ..exceptions.assertion_errors import TassHardAssertionError
from ..exceptions.assertion_errors import TassSoftAssertionError
from ..log.logging import getLogger


class TassCase(TassItem):

    logger = getLogger(__name__)

    def execute_tass(self):
        self._start_time = datetime.now().strftime("%d-%m-%Y--%H_%M_%S")
        self.logger.info("Case: %s (%s) started @%s",
                         self.title, self.uuid, self._start_time)
        self._status = 'incomplete'
        for step, result in zip(self.steps, self._results):
            if step["uuid"] != result["uuid"]:
                raise RuntimeError("Unknown error occured. UUID mismatch detected.")
            self.logger.info("Executing > > > > %s", step['title'])
            self.logger.debug("Parameters > > > > %r", step)
            try:
                # Executing the step, catching the custom exception
                # reporting a failed step here.
                self._execute_step(step, result)
                self.logger.info("Step: %s completed successfully.",
                                 step['title'])
                result.update({"status": "passed"})
            except TassSoftAssertionError as soft_fail:
                # TODO: Error message should be attached here.
                self.logger.warning(
                    (f"Step \"{step['uuid']}\": \"{step['title']}\" "
                     "failed assertion. Stopping test case.")
                     )
                self.logger.warning("Failure message: %s", soft_fail)
                error = {
                    "status": "failed",
                    "status_message": str(soft_fail)
                    }
                # TODO: Do not update step. Convert to step result object/dict
                result.update(error)
                self._errors.append(result)
            except TassHardAssertionError as fail:
                # TODO: Error message should be attached here.
                self.logger.warning(
                    (f"Step \"{step['uuid']}\": \"{step['title']}\" "
                     "failed assertion. Stopping test case.")
                     )
                self.logger.warning("Failure message: %s", fail)
                error = {
                    "status": "failed",
                    "status_message": str(fail)
                    }
                result.update(error)
                self._errors.append(result)
                break
            except Exception as e:
                self.logger.warning(
                    (f"Step \"{step['uuid']}\": \"{step['title']}\" "
                     "failed. Stopping test case.")
                     )
                self.logger.warning("Unexpected error raised. %s - Msg: %s",
                                    e.__class__.__name__,
                                    e)
                error = {
                    "status": "failed",
                    "error": True,
                    "status_message": str(e)
                    }
                result.update(error)
                self._errors.append(result)
                break

        if (len(self._errors) > 0):
            self._status = 'failed'
            self.parent.record_error()
        else:
            self._status = 'passed'

        self._quit_managers()

    def __init__(self, *, steps=[], managers, **kwargs):
        super().__init__(**kwargs)
        self._steps = steps
        self._results = [step | {"status": "untested"} for step in steps]
        self._start_time = 'not started'
        self._status = 'untested'
        self._errors = []
        self._on_failure_hooks = []
        self._managers = managers

    def __repr__(self):
        return (
            f"TassCase(steps={self._steps},"
            f"managers={self._managers}, parent={self.parent}, "
            f"title={self.title}, uuid={self.uuid}, build={self.build}, "
            ")"
            )

    def _quit_managers(self):
        for manager in self._managers.values():
            try:
                manager.quit()
            except NotImplementedError:
                self.logger.debug('Manager (%s) does not have quit function',
                                  manager)

    @property
    def steps(self):
        return self._steps

    @property
    def status(self):
        return self._status

    def toJson(self):
        return {
            "name": self.title,
            "uuid": self.uuid,
            "start_time": self._start_time,
            "status": self._status,
            "errors": self._errors,
            "steps": self._results,
            "managers": self._managers
        }

    def register_on_failure_hook(self, hook):
        self._on_failure_hooks.append(hook)

    def _execute_step(self, step, result):
        raw = step.get('parameters', None)
        if (not isinstance(raw, dict)):
            params = dict(zip(it := iter(raw), it))
        else:
            params = raw
        action = step.get('action')

        self.logger.debug("Action: %s -- Executed with: %r",
                          action, params)

        if (action[0] in self._managers):
            manager = self._managers[action[0]]
            try:
                manager.action(action[1], **params)
            except Exception as e:
                for hook in self._on_failure_hooks:
                    hook(manager, result, self)
                raise e
            return

        self.logger.warning("Action manager not found for: %s", action[0])
