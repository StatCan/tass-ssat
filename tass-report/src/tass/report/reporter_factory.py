import importlib

def get_reporter(type, package, class_name, *args, **kwargs):
    module = importlib.import_module(f".{type}_reporter", package=package)
    return getattr(module, class_name)(*args, **kwargs)