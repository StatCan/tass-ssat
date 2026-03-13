from ..log.logging import getLogger


log = getLogger(__name__)

class DriverScriptExecutor():
    @classmethod
    def execute(cls, func, *args, **kwargs):
        _ = getattr(cls, func, None)
        if not _:
            log.warning("Function %s not found in %s", func, cls.__name__)
            return None
        return _(*args, **kwargs)