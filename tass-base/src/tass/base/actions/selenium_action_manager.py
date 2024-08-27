from .action_manager import ActionManager
from ..drivers.driverconfig import new_driver
from . import selenium as sel
from . import selenium_wait as selwait


def get_manager(config, *args, **kwargs):
    managers = {}
    manager = {
            'config': config,
            'driver': None
            }
    selenium = SeleniumActionManager(manager)
    waiter = SeleniumActionManager(manager, module=selwait)

    managers['selenium'] = selenium
    managers['selwait'] = waiter

    return managers


class SeleniumActionManager(ActionManager):
    def __init__(self, manager, module=sel):
        super().__init__(module) 
        self._manager = manager

    def action(self, command, *args, **kwargs):
        if not self._manager['driver']:
            self._manager['driver'] = new_driver(**self._manager['config'])
        driver = self._manager['driver']
        super().action(command, driver=driver, *args, **kwargs)

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
