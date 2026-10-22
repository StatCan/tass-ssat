from tass.core.exceptions.registry_errors import NoSuchTASSRegistryError as RegistryError, TASSCommandNotFoundError as CommandError
from .registry import Registry
from tass.core.log.logging import getLogger

logger = getLogger(__name__)


class BaseBroker(Registry):
    def __init__(self):
        super().__init__()


class BrokerRegistry(Registry):
    def register(self, name: str, fallback: str, command_module: str, broker: type[BaseBroker], **kwargs):
        if name in self._registry:
            return self.get(name)
        registry = broker(fallback, command_module, **kwargs)
        return super().register(registry, name)

    def get(self, name):
        rx = super().get(name)
        if rx is None:
            raise RegistryError()
        return rx

    def get_command(self, namespace, command):
        return self.get(namespace).get(command)

    # 1. Attempt to resolve command to given namespace
    # 2. Attempt to resolve to specified fallback
    # 3. Attempt to resolve to module default fallback    
    def resolve(self, namespace, command, *, fallback=None, previously=[]):
        fn = None
        def _fallback(fallback):
            if fallback in previously:
                return None
            _previously = previously.copy()
            logger.debug("%s not in %s. Attempting to resolve via fallback: %s", command, namespace, _fallback)
            _previously.append(namespace)
            return self.resolve(fallback, command, previously=_previously)
        try:
            prime = self.get(namespace)
            logger.debug("Resolved %s to %s", namespace, prime._path)
        except RegistryError as e:
            if fallback and fallback is not namespace:
                fn = _fallback(fallback)
            if fn is None:
                raise e

        try:
            fn = prime.get(command)
            logger.debug("Resolved %s in %s", command, namespace)
            return fn
        except CommandError as e:
            fb = prime.fallback or fallback
            if fb and fb is not namespace:
                fn = _fallback(fb)
            if fn is None:
                raise e
        return fn