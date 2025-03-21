import importlib


DEFAULTS = {
    "testrail": {
        "_type": "testrail_reporter",
        "package": "tass.report.testrail",
        "class_name": "TassTestrailReporter"
    }
}

def get_reporter(_type, package=None, class_name=None, *args, **kwargs):
    if (package == None
        and class_name == None
        and _type in DEFAULTS):
        __type, __package, __class_name = (
            DEFAULTS[_type]["_type"],
            DEFAULTS[_type]["package"],
            DEFAULTS[_type]["class_name"]
            )

        return get_reporter(__type, __package, __class_name, *args, **kwargs)
    module = importlib.import_module(f".{_type}", package=package)
    return getattr(module, class_name)(*args, **kwargs)
