class TassAssertionError(Exception):
    def __init__(self, message, reason=None, *args):
        super().__init__()
        self._message = message
        self._reason = reason
        self._args = args

    @property
    def message(self):
        return self._message

    @property
    def reason(self):
        return self._reason

    @property
    def args(self):
        return self._args


class TassSoftAssertionError(TassAssertionError):
    def __init__(self, message, reason=None, *args):
        super().__init__(message, reason, args)


class TassHardAssertionError(TassAssertionError):
    def __init__(self, message, reason=None, *args):
        super().__init__(message, reason, args)
