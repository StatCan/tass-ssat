from ..action_manager import ActionManager
from ...drivers.driverconfig import new_driver
from . import appium as app
from . import appium_wait as appwait
from . import appium_chain as appchain

all_managers = {}


def get_manager(driver_config, *args, **kwargs):
    # TODO: configure settings for drivers.
    if driver_config['uuid'] in all_managers:
        return all_managers[driver_config['uuid']]
    managers = {}
    manager = {
            'config': driver_config,
            'driver': None
            }
    appium = AppiumActionManager(manager)
    waiter = AppiumActionManager(manager, module=appwait)
    chain = AppiumActionManager(manager, module=appchain)

    managers['appium'] = appium
    managers['appwait'] = waiter
    managers['appchain'] = chain

    all_managers[driver_config['uuid']] = managers

    return managers


class AppiumActionManager(ActionManager):
    def __init__(self, manager, module=app):
        super().__init__(module)
        self._manager = manager

    def action(self, command, *args, **kwargs):
        if not self._manager['driver']:
            # TODO: Implement appium new driver function
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
