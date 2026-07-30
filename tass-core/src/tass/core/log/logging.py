import logging
import logging.config
import logging.handlers
from pathlib import Path
from ..context import Context as Ctx


class CustomTassFileLogger(logging.handlers.RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Path(self.baseFilename).exists():
            self.doRollover()


DEFAULT_PATH = "./log"
DEFAULT_NAME = "tass"


RUN_LOGGING_DISABLED = False
TEST_LOGGING_DISABLED = False



def _DEFAULT_CONFIG(log_fldr, log_name, log_level="INFO"):
    log = Path(log_fldr).joinpath(log_name).with_suffix(".log")
    debug = Path(log_fldr).joinpath(log_name+"-debug").with_suffix(".log")
    return {
        "version": 1,
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
            "tass-cli": {
                "class": "logging.StreamHandler",
                "level": log_level, # TODO: set by CMD arg?
                "formatter": "simple"
            },
            "tass-info-file": {
                "()": CustomTassFileLogger,
                "delay": True,
                "filename": f"{log}",
                "encoding": "utf-8",
                "backupCount": 3,
                "level": "INFO",
                "formatter": "simple"
            },
            "tass-debug-file": {
                "()": CustomTassFileLogger,
                "delay": True,
                "filename": f"{debug}",
                "encoding": "utf-8",
                "backupCount": 3,
                "level": "DEBUG",
                "formatter": "detailed"
            }
        },
        "loggers": {
            "tass": {
                "propagate": False,
                "handlers": ["tass-cli", "tass-info-file", "tass-debug-file"],
                "level": "DEBUG"
            }
        }
    }


def init_base_logger(file_name=DEFAULT_NAME, path=DEFAULT_PATH, config={}):
    # Create log folder
    _config = None
    _path = Path(path)
    if not path.endswith("log"):
        _path = _path.joinpath("log")
    _path.resolve().mkdir(parents=True, exist_ok=True)
    log_fldr = _path.resolve()
    log_name = file_name
    _config = _DEFAULT_CONFIG(log_fldr, log_name)
    _config.update(config)
    logging.config.dictConfig(_config)


def init_run_logger():
    # TODO: Create logger specific to the ongoing run.
    pass

def init_test_logger():
    # TODO: Create logger specific to the ongoing run.
    pass


def getLogger(*name):
    if (name[0].startswith('tass')):
        logger = logging.getLogger('.'.join(name))
    else:
        logger = logging.getLogger('.'.join(['tass', *name]))
    return logger
