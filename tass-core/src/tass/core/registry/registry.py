
from ..log.logging import getLogger

logger = getLogger(__name__)


class Registry():
    def __init__(self):
        self._registry = {}

    def register(self, fn, name):
        raise NotImplementedError("register function is not implemented.")
    
    def get(self, name):
        return self._registry.get(name, None)

    def __contains__(self, name):
        return name in self._registry

    @property
    def registry(self):
        return self._registry.keys()


