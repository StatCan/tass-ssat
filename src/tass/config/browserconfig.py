import configparser
import json
from pathlib import Path


# dictionary containing all other configurations.
config_root = './configs'


def load(obj):
    # load defaults for config.
    config = _default_browser_configs()
    if (isinstance(obj, dict)) and ('ref' in obj):
        # TODO: load file from ref
        _p = Path(config_root).resolve().joinpath(obj.get('ref'))
        with open(_p) as file:
            _toload = json.load(file)
            config.read_dict(_toload)
    elif isinstance(obj, dict):
        _toload = obj
        config.read_dict(_toload)

    return config


def _default_browser_configs():
    # Load default browser
    # TODO: update configs defaults through experimentation.
    browsers = configparser.ConfigParser()
    defaults = {
        "DEFAULT": {
            "implicit_wait": 5,
            "explicit_wait": 20,
            "options": ["--start-maximized"],
            "name": "default"
        },
        "chrome": {
            "name": "chrome"
        },
        "firefox": {
            "name": "firefox"
        },
        "edge": {
            "name": "edge"
        },
        "safari": {
            "name": "safari"
        }
    }

    browsers.read_dict(defaults)
    return browsers
