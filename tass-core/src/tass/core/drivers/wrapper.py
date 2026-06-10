import random
import time
from ..log.logging import getLogger


log = getLogger(__name__)


class BaseDriverWrapper():
    def __init__(self, uuid, configs, *args, **kwargs):
        self._conf = self._set_defaults(configs)
        self._uuid = uuid
        self._driver = None


    def _set_defaults(self, configs):
        raise NotImplementedError(
            "This method should be implemented by subclasses"
            )

    def __call__(self, *args, **kwargs):
        # This method should be implemented by subclasses
        # to initialize the driver, as needed, and return it.
        raise NotImplementedError(
            "This method should be implemented by subclasses"
            )

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

    @property
    def uuid(self):
        return self._uuid


class CoreDriverWrapper(BaseDriverWrapper):
    def __init__(self, uuid, configs={}):
        super().__init__(uuid, configs)

    def _set_defaults(self, configs):
        configs.setdefault("driver", {})

    def __call__(self, *args, **kwargs):
        return self._with_delay(self.__driver)
