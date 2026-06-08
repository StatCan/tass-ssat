import importlib
import inspect


def find_hook(module, timing, name, level):
    # Try to import the specified hook module
    func_name = f"tass_{level}_hook_{name}_{timing}"
    mod = importlib.import_module(module)
    if hasattr(mod, func_name):
        func = getattr(mod, func_name)
        if inspect.isfunction(func):
            return func
        else:
            return
