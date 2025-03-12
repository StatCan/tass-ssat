import logging
import logging.config
import json
from pathlib import Path

Path("./log").mkdir(parents=True, exist_ok=True)
CONFIG_PATH = "configs/log-config.json"

path = Path(CONFIG_PATH)

if not path.exists():
    config = {
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
                "filename": "log/tass.log",
                "when": "W0",
                "level": "INFO",
                "formatter": "simple"
            },
            "debug-file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "log/tass-debug.log",
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

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

else:
    with open(path) as f:
        config = json.load(f)

logging.config.dictConfig(config)


def getLogger(*name):
    if (name[0].startswith('tass')):
        logger = logging.getLogger('.'.join(name))
    else:
        logger = logging.getLogger('.'.join(['tass', *name]))
    return logger
