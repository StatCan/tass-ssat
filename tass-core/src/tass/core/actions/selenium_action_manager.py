from .action_manager import ActionManager
from ..drivers.new_driver import new_driver
from . import selenium as sel
from . import selenium_wait as selwait
from . import selenium_chain as selchain

all_managers = {}


def get_manager(browser_config, *args, **kwargs):
    if browser_config['uuid'] in all_managers:
        return all_managers[browser_config['uuid']]
    managers = {}
    manager = {
            'config': browser_config,
            'driver': None
            }
    selenium = SeleniumActionManager(manager)
    waiter = SeleniumActionManager(manager, module=selwait)
    chain = SeleniumActionManager(manager, module=selchain)

    managers['selenium'] = selenium
    managers['selwait'] = waiter
    managers['selchain'] = chain

    all_managers[browser_config['uuid']] = managers

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
