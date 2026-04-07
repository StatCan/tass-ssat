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

    @property
    def alert_text(self):
        log.debug("Getting alert text.")
        return self.alert.text

    @property
    def alert(self):
        log.debug("Getting alert.")
        return self._driver.switch_to.alert

    def accept_alert(self, text=None):
        log.debug("Accepting alert.")
        alert = self.alert
        if text:
            log.debug("Sending text to alert: %s", text)
            alert.send_keys(text)
        return alert.accept()

    def dismiss_alert(self, text=None):
        log.debug("Dismissing alert.")
        alert = self.alert
        if text:
            log.debug("Sending text to alert: %s", text)
            alert.send_keys(text)
        return alert.dismiss()

    @property
    def uuid(self):
        return self._uuid
