import importlib


modules = {
    "selenium":
        'tass.base.actions.selenium_action_manager',
    "core":
        'tass.base.actions.core_action_manager',
    "selwait":
        'tass.base.actions.selenium_action_manager'
}


def get_manager(module_name, **kwargs):
    # Try to import the required module
    module = _import_module(module_name)

    manager = module.get_manager(**kwargs)
    return manager


def _import_module(module_name):
    # If using a standard module, import path is prepared above.
    if module_name in modules:
        imp = modules[module_name]
    else:
        # If using custom module, attempt direct import.
        imp = module_name

    try:
        # Try to import the specified module action manager
        return importlib.import_module(imp)
    except ImportError as e:
        print(e)
        raise e
        # TODO: log error


class ActionManager():
    def __init__(self, module):
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
