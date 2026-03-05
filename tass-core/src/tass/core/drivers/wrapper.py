import random
import time
from ..log.logging import getLogger


log = getLogger(__name__)

class BaseDriverWrapper():
    def __init__(self, uuid, configs, *args, **kwargs):
        self._waits = {}
        self._conf = self._set_defaults(configs)
        self._driver = None
        self._uuid = uuid
        self._chain = None

    def _set_defaults(self, configs):
        raise NotImplementedError("This method should be implemented by subclasses")

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses")

    def _with_delay(self, driver):
        delayMin = abs(float(self._conf['driver'].get('delay', 0)))
        delayMax = abs(float(self._conf['driver'].get('delayMax', delayMin)))
        if delayMax == delayMin or delayMax < delayMin:
            delay = delayMax
        elif delayMax != delayMin:
            delay = round(
                random.uniform(delayMin, delayMax), 2
                )
        if delay > 0:
            log.debug("Delaying for %s seconds.", delay)
            time.sleep(delay)
        return driver

    def _setup(self, function, *args, **kwargs):
        func = getattr(self, function, None)
        if not func:
            log.warning("Function %s not found in driver wrapper: %s", function, self.__class__.__name__)
        return func(*args, **kwargs)
