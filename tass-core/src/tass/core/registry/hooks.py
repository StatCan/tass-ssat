import inspect
from typing import Callable
from dataclasses import dataclass
from collections.abc import Iterable
from functools import wraps
from importlib import import_module
from .broker import BaseBroker
from ..log.logging import getLogger
from tass.core.hooks.hook_cfg import HookEvent
from tass.core.exceptions.hook_errors import HookError

logger = getLogger(__name__)


def _normalize_events(events: HookEvent | str | Iterable[HookEvent | str]):
    allowed = None
    if events is None:
        return frozenset()
    elif isinstance(events, HookEvent):
        allowed = [events]
    elif isinstance(events, str):
        allowed = [HookEvent(events)]
    elif isinstance(events, Iterable):
        allowed = [HookEvent(e.lower()) for e in events]
    return frozenset(allowed)


@dataclass(frozen=True)
class HookDefinition():
    func: Callable
    name: str
    allowed_events: frozenset[HookEvent] | None
    critical: bool

    def __call__(self, *args, **kwds):
        self.func(*args, **kwds)

    def __post_init__(self):
        if not isinstance(self.allowed_events, frozenset) and isinstance(self.allowed_events, Iterable):
            self.allowed_events = frozenset(self.allowed_events)


class HookBroker(BaseBroker):
    def __init__(self, fallback, path):
        super().__init__()
        self._fallback = fallback
        self._path = path

    def get(self, name):
            if not self.registry:
                try:
                    if self._path:
                        import_module(self._path)
                except ImportError as e:
                    logger.error("Unable to import command package: %s.", self._path)
                    logger.error("%s", e)
                    raise e
            fn = super().get(name)
            if fn is None:
                raise HookError()
            return fn

    def hook(self, fn=None, *,
             name: str | None = None,
             events: HookEvent | str | Iterable[HookEvent | str] = None,
             critical: bool = True):
        _allowed = _normalize_events(events)
        def decorator(fn):
            unwrapped = inspect.unwrap(fn)
            _name = name or unwrapped.__name__
            @wraps(fn)
            def wrapper(*args, **kwargs):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    if critical:
                        # TODO: Return critical hook result?
                        pass
                    pass
            
            def_hook = HookDefinition(name=_name,
                                      func=wrapper,
                                      critical=critical,
                                      allowed_events=_allowed)
            return self.register(def_hook, _name).func
        
        if fn:
            return decorator(fn)
        return decorator

