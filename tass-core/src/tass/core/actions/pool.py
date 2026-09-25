import importlib
from tass.core.log.logging import getLogger


log = getLogger(__name__)

modules = {
    "selenium":  # For Backwards Compatibility
    'tass.core.actions.browser.manager.selenium_action_manager',
    "core":  # For Backwards Compatibility
    'tass.core.actions.core.manager.core_action_manager',
    "selwait":  # For Backwards Compatibility
    'tass.core.actions.browser.manager.selenium_action_manager',
    "selchain":  # For Backwards Compatibility
    'tass.core.actions.browser.manager.selenium_action_manager',
    "browser":
    'tass.core.actions.browser.manager.selenium_action_manager',
    "mobile":
    'tass.core.actions.mobile.manager.appium_action_manager'
}


def get_manager(module_name, *args, **kwargs):
    # Try to import the required module
    log.debug("Trying to import %s", module_name)
    module = _import_module(module_name)

    log.debug("Getting manager: %s", module)
    manager = module.get_manager(*args, **kwargs)
    log.debug("Created action manager of type: %s", manager.__class__.__name__)
    return manager


def _import_module(module_name):
    # If using a standard module, import path is prepared above.
    if module_name in modules:
        imp = modules[module_name]
        log.debug("Built-in action manager found")
    else:
        # If using custom module, attempt direct import.
        imp = module_name
        log.debug("No built-in manager found.")

    try:
        # Try to import the specified module action manager
        log.debug("attempting to import manager module from: %s", imp)
        return importlib.import_module(imp)
    except ImportError as e:
        print(e)
        raise e
        # TODO: log error

class ExecutorPool():
    def __init__(self):
        self._pool = {}

    def get(self, uuid: str, **manager):
        # TODO: catch key errors
        if uuid not in self._pool:
            _ = get_manager(**manager) or None
            if _:
                self._pool[uuid] = _
            else:
                return None
        return self._pool[uuid]
