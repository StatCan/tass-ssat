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

class AndroidDriver(MobileDriver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_element(self, by, value):
        rect, element = super().find_element(by, value)
        self.logger.debug("Android driver found element >>> tag: %s, location: %s",
                          element.tag_name, rect)
        return element

class IOSDriver(MobileDriver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_element(self, by, value):
        rect, element = super().find_element(by, value)
        self.logger.debug("IOS driver found element >>> tag: %s, location: %s",
                          element.tag_name, rect)
        return element