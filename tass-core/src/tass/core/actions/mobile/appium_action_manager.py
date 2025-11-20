from ..action_manager import ActionManager
from ...drivers.new_driver import new_driver
from . import appium as app
from . import appium_wait as appwait
from . import appium_chain as appchain
from ..browser import selenium as sel
from ..browser import selenium_wait as selwait
from ..browser import selenium_chain as selchain

all_managers = {}


def get_manager(mobile_configs, *args, **kwargs):
    breakpoint()
    # TODO: configure settings for drivers.
    if mobile_configs['uuid'] in all_managers:
        return all_managers[mobile_configs['uuid']]
    managers = {}
    manager = {
            'config': mobile_configs,
            'driver': None
            }
    appium = AppiumActionManager(manager)
    waiter = AppiumActionManager(manager, module=appwait)
    chain = AppiumActionManager(manager, module=appchain)

    selenium = AppiumActionManager(manager, module=sel)
    s_waiter = AppiumActionManager(manager, module=selwait)
    s_chain = AppiumActionManager(manager, module=selchain)

    managers['appium'] = appium
    managers['appwait'] = waiter
    managers['appchain'] = chain

    managers['selenium'] = selenium
    managers['selwait'] = s_waiter
    managers['selchain'] = s_chain


    all_managers[mobile_configs['uuid']] = managers

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
