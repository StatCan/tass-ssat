
from ..log.logging import getLogger

logger = getLogger(__name__)


class Registry():
    def __init__(self):
        self._registry = {}

    def register(self, registrant, name):
        self._registry[name] = registrant
        logger.debug("%s registered: %s", self.__class__.__name__, name)
        return registrant
    
    def get(self, name):
        return self._registry.get(name, None)

    def __contains__(self, name):
        return name in self._registry

    @property
    def registry(self):
        return self._registry.keys()


