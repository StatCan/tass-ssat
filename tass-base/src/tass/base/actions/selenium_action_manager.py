from .action_manager import ActionManager
from ..drivers.browserdriver import new_driver
from . import selenium as sel
from . import selenium_wait as selwait


class SeleniumActionManager(ActionManager):
    def __init__(self, browser, config):
        print("started selenium action manager")
        super().__init__(sel)
        self._driver = new_driver(browser, config)

    def wait_manager(self):
        return SeleniumActionManager.SeleniumWaitActionManager(self._driver)

    def action(self, command, *args, **kwargs):
        super().action(command, driver=self._driver, *args, **kwargs)

    def quit(self):
        self._driver.quit()

    class SeleniumWaitActionManager(ActionManager):
        def __init__(self, driver):
            super().__init__(selwait)
            self._driver = driver

        def action(self, command, *args, **kwargs):
            super().action(command, driver=self._driver, *args, **kwargs)
