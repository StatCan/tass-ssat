import logging
import logging.config
import json
import logging.handlers
from pathlib import Path


class CustomTassFileLogger(logging.handlers.RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Path(self.baseFilename).exists():
            self.doRollover()



DEFAULT_PATH = "./log"
DEFAULT_NAME = "tass"
def DEFAULT_CONFIG(log_fldr, log_name):
    log = Path(log_fldr).joinpath(log_name).with_suffix(".log")
    debug = Path(log_fldr).joinpath(log_name+"-debug").with_suffix(".log")
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(levelname)s >>> %(message)s",
                "datefmt": "%d-%m-%y -- %H:%M:%S"
            },
            "detailed": {
                "format": (
                    "%(asctime)s - %(name)s:"
                    "%(funcName)s:%(lineno)s -- "
                    "%(levelname)s >>> %(message)s"
                    )
            }
        },
        "handlers": {
            "cli": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple"
            },
            "info-file": {
                "()": CustomTassFileLogger,
                "delay": True,
                "filename": f"{log}",
                "backupCount": 3,
                "level": "INFO",
                "formatter": "simple"
            },
            "debug-file": {
                "()": CustomTassFileLogger,
                "delay": True,
                "filename": f"{debug}",
                "backupCount": 3,
                "level": "DEBUG",
                "formatter": "detailed"
            }
        },
        "loggers": {
            "tass": {
                "handlers": ["cli", "info-file", "debug-file"],
                "level": "DEBUG"
            }
        }
    }

def init_logger(file_name=DEFAULT_NAME, path=DEFAULT_PATH, config=None):
    # Create log folder
    _config = None
    if not config:
        _path = Path(path)
        if not path.endswith("log"):
            _path = _path.joinpath("log")
        _path.resolve().mkdir(parents=True, exist_ok=True)
        log_fldr = _path.resolve()
        log_name = file_name
        _config = DEFAULT_CONFIG(log_fldr, log_name)
    else:
        _config = config
    logging.config.dictConfig(_config)


def getLogger(*name):
    if (name[0].startswith('tass')):
        logger = logging.getLogger('.'.join(name))
    else:
        logger = logging.getLogger('.'.join(['tass', *name]))
    return logger
