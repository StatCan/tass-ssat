from ....action_manager import ActionExecutor
from ....drivers.new_driver import new_driver
from ....registry import CommandBrokers as executor


def get_manager(mobile_configs, *args, **kwargs):
    managers = {}
    manager = {
            'config': mobile_configs,
            'driver': None
            }

    _ = AppiumActionExecutor(manager)

    managers['appium'] = _
    managers['appwait'] = _
    managers['appchain'] = _

    return managers


class AppiumActionExecutor(ActionExecutor):
    def __init__(self, manager):
        super().__init__(module)
        self._manager = manager

    def action(self, command, *args, **kwargs):
        if not self._manager['driver']:
            self._manager['driver'] = new_driver(**self._manager['config'])
        driver = self._manager['driver']
        executor.resolve(namespace, command)(driver=driver, *args, **kwargs)

    def toJson(self):
        j = super().toJson()
        j2 = {
            "browser": self._manager['config']
        }
        j.update(j2)
        return j

    def quit(self):
        if self._manager['driver']:
            self._manager['driver'].quit()
            self._manager['driver'] = None
