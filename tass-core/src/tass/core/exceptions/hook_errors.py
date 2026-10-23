from .tass_errors import TassException
from tass.core.hooks import HookEvent


class HookError(TassException):
    def __init__(self, message, *args):
        super().__init__(message, *args)
    

class HookBaseExecutionError(HookError):
    def __init__(self, message, event: HookEvent, errors: Exception | list[Exception], *args):
        super().__init__(message, *args)
        self._event = event
        self._errors = errors


class HookExecutionError(HookBaseExecutionError):
    def __init__(self, message, event: HookEvent, errors: Exception | list[Exception], *args):
        super().__init__(message, event, errors, *args)


class CriticalHookExecutionError(HookBaseExecutionError):
    def __init__(self, message, event: HookEvent, errors: Exception | list[Exception], *args):
        super().__init__(message, event, errors, *args)


class HookDefinitionError(HookError):
    def __init__(self, message, *args):
        super().__init__(message, *args)