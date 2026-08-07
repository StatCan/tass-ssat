from contextvars import ContextVar
from ..tools.singleton import Singleton


class TassContextManager(metaclass=Singleton):
    def __init__(self):
        self._vars = {}

    def var(self, name: str, default=None):
        if name not in self._vars:
            self._vars[name] = TassContextVar(name, default=default)
        return self._vars[name]

    def reset_all(self):
        for var in self._vars.values():
            var.reset()

    @property
    def run_uuid(self):
        return self.var("run_uuid", None)

    @property
    def run_id(self):
        return self.var("run_id", None)

    @property
    def run_name(self):
        return self.var("run_name", None)

    @property
    def test_uuid(self):
        return self.var("test_uuid", None)

    @property
    def test_id(self):
        return self.var("test_id", None)

    @property
    def test_name(self):
        return self.var("test_name", None)

    @property
    def driver(self, driver):
        _ = f"driver:{driver}"
        return self.var(_, None)


class TassContextVar():
    def __init__(self, name: str, default=None):
        self._token = None
        self._ctx = ContextVar(name, default=default)

    @property
    def token(self):
        return self._token

    @property
    def value(self):
        return self._ctx.get()

    @value.setter
    def value(self, value):
        self._token = self._ctx.set(value)

    def reset(self):
        if self._token is not None:
            self._ctx.reset(self._token)