import inspect
from enum import Enum
from collections.abc import Iterable
from functools import wraps
from importlib import import_module
from .broker import BaseBroker
from ..log.logging import getLogger
from tass.core.hooks import HookEvent, HookResult

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


class HookBroker(BaseBroker):
    def __init__(self, fallback, path):
        super().__init__()
        self._fallback = fallback
        self._path = path

    def hook(self, fn=None, *,
             name: str | None = None,
             events: HookEvent | str | Iterable[HookEvent | str] = None,
             critical: bool = False):
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
            
            def_hook = {"func": wrapper, "allowed_events": _allowed}
            return self.register(def_hook, _name)
        
        if fn:
            return decorator(fn)
        return decorator

