import importlib


def get_manager(module_name, **kwargs):
    module = _import_module(module_name)
    manager = getattr(module, f'{module_name.capitalize()}ActionManager')
    return manager(**kwargs)


def _import_module(module_name):
    try:
        imp = f"tass.base.actions.{module_name}_action_manager"
        return importlib.import_module(imp)
        # TODO: Import module
    except ImportError as e:
        print(e)
        raise e
        # TODO: log error
        # TODO: try to install?


class ActionManager():
    def __init__(self, module):
        self._module = module

    def action(self, command, *args, **kwargs):
        _action = getattr(self._module, command)
        return _action(*args, **kwargs)

    def quit(self):
        raise NotImplementedError('quit function not implemented')
