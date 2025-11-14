import importlib
from tass.core.log.logging import getLogger


log = getLogger(__name__)

modules = {
    "selenium": # For Backwards Compatibility
        'tass.core.actions.selenium_action_manager', 
    "core": # For Backwards Compatibility
        'tass.core.actions.core_action_manager',
    "selwait": # For Backwards Compatibility
        'tass.core.actions.selenium_action_manager',
    "selchain": # For Backwards Compatibility
        'tass.core.actions.selenium_action_manager',
    "browser":
        'tass.core.actions.selenium_action_manager'
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


class ActionManager():
    def __init__(self, module):
        self._log = getLogger(__class__.__name__)
        self._module = module

    def action(self, command, *args, **kwargs):
        _action = getattr(self._module, command)
        return _action(*args, **kwargs)

    def toJson(self):
        return {
            "type": self.__class__.__name__,
            "module": self._module.__name__
            }

    def quit(self):
        # Method called at the end of every case
        # include any cleanup/resetting required
        # to make each case encapsulated.
        raise NotImplementedError('quit function not implemented')
