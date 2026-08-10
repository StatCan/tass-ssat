import logging
import logging.config
import logging.handlers
from pathlib import Path
from datetime import datetime
from ..context import Context as Ctx
from copy import copy


DEFAULT_PATH = "./log"
DEFAULT_LOG_LEVEL = "INFO"

RUN_LOGGING_DISABLED = False
TEST_LOGGING_DISABLED = False

class TassTestFilter(logging.Filter):
    def filter(self, record):
        if TEST_LOGGING_DISABLED:
            return False
        _id = Ctx().test_id.value
        if _id is None:
            return False

        _name = Ctx().test_name.value or "XtestX"
        _uuid = Ctx().test_uuid.value

        _ = copy(record)
        _.id = _id
        _.name = f"{_name}--{_uuid}".replace(".", "_")
        return _

class TassRunFilter(logging.Filter):
    def filter(self, record):
        if RUN_LOGGING_DISABLED:
            return False
        _id = Ctx().run_id.value
        if _id is None:
            return False

        _name = Ctx().run_name.value or "XrunX"
        _uuid = Ctx().run_uuid.value

        _ = copy(record)
        _.id = _id
        _.name = f"{_name}--{_uuid}".replace(".", "_")
        return _


class CustomTassSessionHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Path(self.baseFilename).exists():
            self.doRollover()


class CustomTassFileHandler(logging.Handler):
    def __init__(self, path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active = {}
        self._dir = path

    def emit(self, record):
        _id = record.id
        handler = self._active.get(_id, None)
        if handler is None:
            name = f"{record.name}--{datetime.now().strftime("%y%m%d_%H%M%S")}"
            path = self._dir.joinpath(name).with_suffix(".log")
            path.parent.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(path, encoding="utf-8")
            handler.setFormatter(self.formatter)
            self._active[_id] = handler
        handler.emit(record)

    def close_file(self, id):
        _ = self._active.pop(id, None)
        if _:
            _.close()

    def close(self):
        for _ in self._active.values():
            _.close()
        self._active.clear()



def _DEFAULT_CONFIG(log_fldr, log_name, log_level):
    log = Path(log_fldr).joinpath(log_name).with_suffix(".log")
    debug = Path(log_fldr).joinpath(log_name).with_suffix(".debug.log")
    runs = Path(log_fldr).joinpath("runs")
    tests = Path(log_fldr).joinpath("tests")
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
        "filters": {
            "run-filter": {
                "()": TassRunFilter
            },
            "test-filter": {
                "()": TassTestFilter
            }
        },
        "handlers": {
            "tass-cli": {
                "class": "logging.StreamHandler",
                "level": log_level, # TODO: set by CMD arg?
                "formatter": "simple"
            },
            "tass-info-file": {
                "()": CustomTassSessionHandler,
                "delay": True,
                "filename": f"{log}",
                "encoding": "utf-8",
                "backupCount": 3,
                "level": "INFO",
                "formatter": "simple"
            },
            "tass-debug-file": {
                "()": CustomTassSessionHandler,
                "delay": True,
                "filename": f"{debug}",
                "encoding": "utf-8",
                "backupCount": 3,
                "level": "DEBUG",
                "formatter": "detailed"
            },
            "tass-run": {
                "()": CustomTassFileHandler,
                "path": runs,
                "level": log_level,
                "formatter": "simple",
                "filters": ["run-filter"]
            },
            "tass-test": {
                "()": CustomTassFileHandler,
                "path": tests,
                "level": log_level,
                "formatter": "simple",
                "filters": ["test-filter"]
            }

        },
        "loggers": {
            "tass": {
                "propagate": False,
                "handlers": ["tass-cli", "tass-info-file", "tass-debug-file", "tass-run", "tass-test"],
                "level": "DEBUG"
            }
        }
    }


def init_base_logger(log_level=DEFAULT_LOG_LEVEL,
                     path=DEFAULT_PATH,
                     run_logging=False,
                     test_logging=False,
                     config={}):
    # Create log folder
    _config = None
    _path = Path(path)
    if not path.endswith("log"):
        _path = _path.joinpath("log")
    log_fldr = _path.resolve()
    log_fldr.mkdir(parents=True, exist_ok=True)
    log_name = "tass-session"
    _config = _DEFAULT_CONFIG(log_fldr, log_name, log_level)
    _config.update(config)
    logging.config.dictConfig(_config)

    global RUN_LOGGING_DISABLED
    global TEST_LOGGING_DISABLED

    RUN_LOGGING_DISABLED = run_logging
    TEST_LOGGING_DISABLED = test_logging


def getLogger(*name):
    if (name[0].startswith('tass')):
        logger = logging.getLogger('.'.join(name))
    else:
        logger = logging.getLogger('.'.join(['tass', *name]))
    return logger

def closeLoggerFile(id):
    logger = getLogger("tass")
    for _ in logger.handlers:
        if isinstance(_, CustomTassFileHandler):
            _.close_file(id)
