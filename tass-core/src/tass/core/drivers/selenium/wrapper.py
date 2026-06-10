from ..wrapper import BaseDriverWrapper
from ...log.logging import getLogger


log = getLogger(__name__)


class BaseSeleniumDriverWrapper(BaseDriverWrapper):
    def __init__(self, uuid, configs, *args, **kwargs):
        super().__init__(uuid, configs, *args, **kwargs)
        self._chain = None
        self._waits = {}

    @property
    def alert_text(self):
        log.debug("Getting alert text.")
        return self.alert.text

    @property
    def alert(self):
        log.debug("Getting alert.")
        return self().switch_to.alert

    def screenshot(self, output, element=None):
        if element:
            status = element.screenshot(output)
        else:
            status = self._driver.save_screenshot(output)
        return status

    def switch_window(self, handle):
        log.debug("Switching to window handle: %s", handle)
        self().switch_to.window(handle)
        log.debug(
            "Switched to window handle: %s",
            handle
            )

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

