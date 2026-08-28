from ..log.logging import getLogger
from importlib import import_module

logger = getLogger(__name__)


class Registry():
    def __init__(self):
        self._registry = {}

    def register(self, name):
        raise NotImplementedError("register function is not implemented.")
    
    def get(self, name):
        return self._registry.get(name, None)

    def __contains__(self, name):
        return name in self._registry

    @property
    def registry(self):
        return self._registry.keys()


class CommandRegistry(Registry):
    def __init__(self, fallback, path):
        super().__init__()
        self._path = path
        self._fallback = fallback

    def command(self, name):
        return self.register(name)

    @property
    def fallback(self):
        return self._fallback

    def get(self, name):
        if not self.registry:
            try:
                if self._path:
                    import_module(self._path)
            except ImportError as e:
                logger.error("Unable to import command package: %s.", self._path)
                raise e
        return super().get(name)

    def register(self, name):
        def decorator(func):
            if name in self._registry:
                # TODO: Raise error on duplicates
                pass
            self._registry[name] = func
            logger.debug("%s registered: %s", self.__class__.__name__, name)
            return func
        return decorator

class CommandModuleRegistry(Registry):
    def register(self, name, fallback, command_module: str):
        if name in self._registry:
            return self.get(name)
        registry = CommandRegistry(fallback, command_module)
        self._registry[name] = registry
        logger.debug("%s module registered as: %s", command_module, name)
        return registry

    def get_command(self, namespace, command):
        return self.get(namespace).get(command)

    # 1. Attempt to resolve command to given namespace
    # 2. Attempt to resolve to specified fallback
    # 3. Attempt to resolve to module default fallback
    def resolve(self, command, namespace, fallback=None, previously=[]):
        prime = self.get(namespace)
        if command in prime:
            logger.debug("Resolved %s in %s", command, namespace)
            return prime.get(command)
        _fallback = fallback or prime.fallback
        if _fallback and _fallback != namespace and namespace not in previously:
            _previously = previously.copy()
            logger.debug("%s not in %s. Attempting to resolve via fallback: %s", command, namespace, _fallback)
            _previously.append(namespace)
            breakpoint()
            return self.resolve(command=command, namespace=_fallback)
        # TODO: Raise resolution error
