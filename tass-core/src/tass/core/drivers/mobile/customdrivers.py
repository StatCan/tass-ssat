import time
import enum
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from ...log.logging import getLogger


class TassMobileDriverWait(WebDriverWait):
    def __init__(self, driver,
                 timeout,
                 poll_frequency,
                 ignored_exceptions):
        super().__init__(driver, timeout, poll_frequency, ignored_exceptions)

        self.logger = getLogger(__name__, driver.name, 'wait')
        self.logger.debug("Creating new wait driver with timeout of: %d",
                          float(timeout)
                          )


class MobileDriver(webdriver.Remote):
    """ Custom SafariDriver for selenium interactions."""

    NATIVE = "NATIVE_APP"
    CHROME = "WEBVIEW_chrome"

    def __init__(self, options,
                 url_base="http://localhost",
                 port=4723,
                 *args, **kwargs):
        server_url = f"{url_base}:{port}"
        super().__init__(server_url, options=options, *args, **kwargs)
        self.logger = getLogger(__name__, self.name)

    def find_element(self, by, value):
        element = super().find_element(by, value)
        if element.is_displayed():
            rect = element.rect
        else:
            rect = {
                "height": 0,
                "width": 0,
                "x": 0,
                "y": 0
            }

        return rect, element

    def toJson(self):
        return self.capabilities
    
    def find_webview_context(self):
        for _ in range(5):
            for ctx in self.contexts:
                if "WEBVIEW" in ctx:
                    return ctx
            time.sleep(0.5)
        # TODO: handle edgecase where no Webview context present

    def switch_to_context(self, context):
        found = False
        for _ in range(5):
            if context in self.contexts:
                found = True
                break
            else:
                time.sleep(0.5)
        # TODO: handle edgecase where context not present
        if found:
            self.switch_to.context(context)

class AndroidDriver(MobileDriver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_element(self, by, value):
        rect, element = super().find_element(by, value)
        self.logger.debug("Android driver found element >>> tag: %s, location: %s",
                          element.tag_name, rect)
        return element

    def hide_keyboard(self, strategy="back", *args, **kwargs):
        def back(*args, **kwargs):
            # Hiding the keyboard by tapping the android back button
            if self.is_keyboard_shown:
                # If keyboard is not displayed, do not use the "back" button
                self.logger.debug("Virtual keyboard is not displayed")
                return
            # Save the current context to switch back quickly
            curr = self.current_context
            self.logger.debug("Current context is: %s", curr)
            if curr != self.NATIVE:
                # Switch to NATIVE context to interact with android back button
                self.logger.debug("Switching to %s context", self.NATIVE)
                self.switch_to_context(self.NATIVE)
            
            self.logger.info("Closing virtual keyboard with back button")
            self.back()

            if curr != self.current_context:
                # Return to the original context for ease of use.
                self.logger.debug("Switching back to %s context", curr)
                self.switch_to_context(curr)
        
        def default(*args, **kwargs):
            # Use the default android hide_keyboard strategy.
            super().hide_keyboard()

        valid_strategies = {
            "back": back,
            "default": default
        }


        hide = valid_strategies.get(strategy, None)
        if not hide:
            self.logger.warning("\"%s\" is not a valid strategy. Using \"back\" strategy.", strategy)
            hide = back
        hide(*args, **kwargs)

        if self.is_keyboard_shown:
            self.logger.warning("Keyboard failed to close")
            return False
        else:
            self.logger.info("Virtual keyboard close")
            return True


class IOSDriver(MobileDriver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_element(self, by, value):
        rect, element = super().find_element(by, value)
        self.logger.debug("IOS driver found element >>> tag: %s, location: %s",
                          element.tag_name, rect)
        return element