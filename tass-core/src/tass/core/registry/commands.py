from functools import wraps
from importlib import import_module
from exceptiongroup import ExceptionGroup
import inspect

from .broker import BaseBroker
from tass.core.log.logging import getLogger
from tass.core.exceptions.registry_errors import TASSCommandNotFoundError as CommandError



logger = getLogger(__name__)


class FinderBroker(BaseBroker):
    def __init__(self, module: str):
        super().__init__()
        self._path = module
    
    def finder(self, fn=None, *, name):
        def decorator(fn):
            unwrapped = inspect.unwrap(fn)
            _name = name or unwrapped.__name__
            @wraps(fn)
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs)
            return self.register(wrapper, _name)
        if fn:
            return decorator(fn)
        return decorator 

    def get(self, name):
        if not self.registry:
            import_module(self._path)
        return super().get(name)


class CommandBroker(BaseBroker):
    def __init__(self, fallback, 
                 path: str,
                 default_retries: int=0):
        super().__init__()
        self._path = path
        self._fallback = fallback
        self._default_retries = default_retries      

    # Decorator for callable tass commands.
    def command(self, fn=None, *,
                name=None,
                additional: set[str]=set(),
                retries: int=None,
                retry_exc: list[Exception]=[]):
        def decorator(fn):
            unwrapped = inspect.unwrap(fn)
            params = inspect.signature(unwrapped).parameters
            is_kwargs = any(
                p.kind == inspect.Parameter.VAR_KEYWORD
                for p in params.values()
            )
            valid_params = set(params.keys()) | additional
            allowable_exc = retry_exc
            _name = name or unwrapped.__name__
            retry_max = retries or self._default_retries

            @wraps(fn)
            def wrapper(*args, **kwargs):
                if args:
                    logger.warning("%s - Positional arguments cannot be verified or filtered. Use at own risk", _name)
                    logger.warning(args)
                retry_override = kwargs.pop("retries", None) or retry_max
                if is_kwargs and not additional:
                    return self._with_retry(fn, retry_override, allowable_exc, *args, **kwargs)

                filtered, discarded = self._filter(valid_params, **kwargs)
                for k in discarded:
                    logger.warning("Invalid parameter: %s removed from: %s", k, unwrapped.__name__)
                return self._with_retry(fn, retry_override, retry_exc, *args, **filtered)
            self.register(wrapper, _name)
            return wrapper
        if fn:
            return decorator(fn)
        return decorator

    def _with_retry(self, fn, retry_max, retry_exc, *args, **kwargs):
        if not retry_max or not retry_exc:
            logger.debug("Starting attempt without retries for %s", fn.__name__)
            return fn(*args, **kwargs)
        expected_errors = tuple(retry_exc)
        caught_errors = []
        last_exc = None
        attempts = 0
        while attempts <= retry_max:
            attempts += 1
            try:
                logger.debug("Starting attempt %d for %s", attempts, fn.__name__)
                _ = fn(*args, **kwargs)
                logger.debug("Completed %s on attempt %d", fn.__name__, attempts)
                return _
            except expected_errors as e:
                logger.warning("Something went wrong with %s: %s -- Trying again", fn.__name__, e)
                caught_errors.append(e)
                last_exc = e
        if len(caught_errors)>1:
            raise ExceptionGroup(f"Several errors occured during {attempts} attempts: {fn.__name__}", caught_errors)
        logger.error("Failed to complete %s after %s attempts due to: %s", fn.__name__, attempts, last_exc)
        raise last_exc

    def _filter(self, valid_params, **kwargs):
            filtered = {}
            discarded = []
            for k, v in kwargs.items():
                if k in valid_params:
                    filtered[k] = v
                else:
                    discarded.append(k)
            return filtered, discarded

    def register(self, fn, name):
        if name in self._registry:
            # TODO: Raise error on duplicates
            pass
        return super().register(fn, name)

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
                logger.error("%s", e)
                raise e
        fn = super().get(name)
        if fn is None:
            raise CommandError()
        return fn


class SeleniumCommandBroker(CommandBroker):
    def __init__(self, fallback, 
                 path: str,
                 default_retries: int=0,
                 finder: FinderBroker=None):
        super().__init__(fallback, path, default_retries)
        self._finder = finder

    # Decorator to define finding function
    def find_with(self, fn=None, *,
                  finder: str):
        default_finder = finder
        def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                if not callable(kwargs.get("find", None)):
                    fkey = kwargs.pop("find", default_finder)
                    kwargs["find"] = self._finder.get(fkey)
                return fn(*args, **kwargs)
            return wrapper
        if fn:
            return decorator(fn)
        return decorator 