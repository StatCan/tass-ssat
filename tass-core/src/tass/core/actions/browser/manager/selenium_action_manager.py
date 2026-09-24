from ...action_manager import ActionExecutor
from ....drivers.new_driver import new_driver
from ....registry import CommandBrokers as executor


def get_manager(browser_config, *args, **kwargs):
    if "driver_name" not in browser_config:
        # Backwards compatible with old config naming
        browser_config["driver_name"] = browser_config["browser_name"]
    managers = {}
    manager = {
            'config': browser_config,
            'driver': None
            }

    _ = SeleniumActionExecutor(manager)

    managers['selenium'] = _
    managers['selwait'] = _
    managers['selchain'] = _

    return managers


class SeleniumActionExecutor(ActionExecutor):
    def __init__(self, manager):
        super().__init__()
        self._manager = manager

    def action(self, namespace, command, *args, **kwargs):
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
