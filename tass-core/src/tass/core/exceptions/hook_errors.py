from .tass_errors import TassException


class HookError(TassException):
    def __init__(self, message, *args):
        super().__init__(message, *args)
    

class HookExecutionError(HookError):
    def __init__(self, message, errors: Exception | list[Exception], *args):
        super().__init__(message, *args)
        self._errors = errors


class CriticalHookExecutionError(HookExecutionError):
    def __init__(self, message, errors: Exception | list[Exception], *args):
        super().__init__(message, errors, *args)


class HookDefinitionError(HookError):
    def __init__(self, message, *args):
        super().__init__(message, *args)