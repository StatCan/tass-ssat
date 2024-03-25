from .action_manager import ActionManager
from ..drivers.browserdriver import new_driver
from . import selenium as sel
from . import selenium_wait as selwait


def get_manager(browser, config):
    managers = {}
    manager = {
            'browser': browser,
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
            self._manager['driver'] = new_driver(
                                            self._manager['browser'],
                                            self._manager['config'])
        driver = self._manager['driver']
        super().action(command, driver=driver, *args, **kwargs)

    def quit(self):
        if self._manager['driver']:
            self._manager['driver'].quit()
            self._manager['driver'] = None
