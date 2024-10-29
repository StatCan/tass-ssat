class TassError(Exception):
    def __init__(self, message, reason, *args):
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