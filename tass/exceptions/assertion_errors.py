class TassAssertionError(Exception):
    def __init__(self, message, reason=None, *args):
        super().__init__()
        self.message = message
        self.reason = reason
        self.args = args


class TassSoftAssertionError(TassAssertionError):
    def __init__(self, message, reason=None, *args):
        super().__init__(message, reason, args)
