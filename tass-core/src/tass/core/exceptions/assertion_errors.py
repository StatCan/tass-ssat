from .tass_errors import TassException


class TassAssertionError(TassException):
    def __init__(self, message, reason, *args):
        super().__init__(message, *args)
        self._reason = reason

    @property
    def reason(self):
        return self._reason or self.__cause__


class TassSoftAssertionError(TassAssertionError):
    def __init__(self, message, reason=None, *args):
        msg = None
        if not reason:
            msg = f"Soft assertion failed: {message}"
        else:
            msg = f"Soft assertion failed: {message} -- by reason of: {reason}"

        super().__init__(msg, reason, *args)


class TassHardAssertionError(TassAssertionError):
    def __init__(self, message, reason=None, *args):
        msg = None
        if not reason:
            msg = f"Hard assertion failed: {message}"
        else:
            msg = f"Hard assertion failed: {message} -- by reason of: {reason}"
        super().__init__(msg, reason, *args)
