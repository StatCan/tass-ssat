from .tass_errors import TassException


class TassAssertionError(TassException):
    def __init__(self, message, reason, *args):
        super().__init__(message, *args)
        self._reason = reason # The error or exception that caused the failure if applicable.

    @property
    def reason(self):
        return self._reason


class TassSoftAssertionError(TassAssertionError):
    def __init__(self, message, reason=None, *args):
        super().__init__(message, reason, *args)


class TassHardAssertionError(TassAssertionError):
    def __init__(self, message, reason=None, *args):
        super().__init__(message, reason, *args)
