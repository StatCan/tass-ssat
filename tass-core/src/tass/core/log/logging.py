import logging
import logging.config
import json
from pathlib import Path


log_fldr = None
DEFAULT_PATH = "./logs"
DEFAULT_CONFIG = {
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
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": f"{log_fldr}/tass.log",
            "when": "W0",
            "level": "INFO",
            "formatter": "simple"
        },
        "debug-file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": f"{log_fldr}/tass-debug.log",
            "when": "D",
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

def init_logger(path=DEFAULT_PATH, config=DEFAULT_CONFIG):
    # Create log folder
    _path = Path(path)
    if not path.endswith("log"):
        _path.joinpath("log")
    _path.mkdir(parents=True, exist_ok=True)


def getLogger(*name):
    if (name[0].startswith('tass')):
        logger = logging.getLogger('.'.join(name))
    else:
        logger = logging.getLogger('.'.join(['tass', *name]))
    return logger
