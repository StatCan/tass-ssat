from ..action_manager import ActionManager
from . import selenium as sel
from . import selenium_wait as selwait
from . import selenium_chain as selchain

all_managers = {}


def get_manager(browser_config, *args, **kwargs):
    if browser_config['uuid'] in all_managers:
        return all_managers[browser_config['uuid']]
    if "driver_name" not in browser_config:
        # Backwards compatible with old config naming
        browser_config["driver_name"] = browser_config["browser_name"]
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
        super().__init__(module, manager)

    def action(self, command, *args, **kwargs):
        super().action(command, driver=self.driver, *args, **kwargs)

    def toJson(self):
        j = super().toJson()
        j2 = {
            "browser": self._manager['config']
        }
        j.update(j2)
        return j

    def quit(self):
        if self.driver:
            self.driver.quit()
            del self.driver
