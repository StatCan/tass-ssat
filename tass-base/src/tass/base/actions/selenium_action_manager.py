from .action_manager import ActionManager
from ..drivers.browserdriver import new_driver
from . import selenium as sel
from . import selenium_wait as selwait


def get_manager(browser, config):
    managers = {}
    selenium = SeleniumActionManager(browser, config)
    waiter = selenium.wait_manager()

    managers['selenium'] = selenium
    managers['selwait'] = waiter

    return managers


class BrowserDriverActionManager(ActionManager):
    def __init__(self, module, manager):
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


class SeleniumActionManager(BrowserDriverActionManager):
    def __init__(self, browser, config):
        manager = {
            'browser': browser,
            'config': config,
            'driver': None
            }
        super().__init__(sel, manager)

    def wait_manager(self):
        return SeleniumWaitActionManager(self._manager)


class SeleniumWaitActionManager(BrowserDriverActionManager):
    def __init__(self, manager):
        super().__init__(selwait, manager)
