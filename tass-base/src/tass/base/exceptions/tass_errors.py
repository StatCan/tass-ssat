class TassException(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)

    @property
    def message(self):
        return self.args[0].format(*self.args[1:])
        


class TassUUIDEexception(TassError):
    def __init__(self, message, *args):
        super().__init__(message, *args)


class TassUUIDNotFound(TassUUIDEexception):
    def __init__(self, uuid):
        message = "Given UUID: {} was not found."
        super().__init__(message, uuid)


class TassAmbiguousUUID(TassUUIDEexception):
    def __init__(self, uuid):
        message = "Given UUID: {} is ambiguous. Associated value is not unique."
        super().__init__(message, uuid)
        

    