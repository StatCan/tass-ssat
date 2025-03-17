from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from ..log.logging import getLogger


class TassDriverWait(WebDriverWait):
    def __init__(self, driver,
                 timeout,
                 poll_frequency,
                 ignored_exceptions):
        super().__init__(driver, timeout, poll_frequency, ignored_exceptions)

        self.logger = getLogger(__name__, driver.name, 'wait')
        self.logger.debug("Creating new wait driver with timeout of: %d",
                          float(timeout)
                          )


class ChromeDriver(webdriver.Chrome):
    """ Custom ChromeDriver for selenium interactions."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = getLogger(__name__, self.name)

    def find_element(self, by, value):
        element = super().find_element(by, value)
        self.logger.debug("Chrome found element >>> tag: %s, location: %s",
                          element.tag_name, element.rect)
        return element

    def toJson(self):
        caps = self.capabilities
        return {
            'name': caps['browserName'],
            'version': caps['browserVersion'],
            'driver-version': caps['chrome']['chromedriverVersion'],
            'platform': caps['platformName']
        }


class FirefoxDriver(webdriver.Firefox):
    """ Custom FirefoxDriver for selenium interactions."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = getLogger(__name__, self.name)

    def find_element(self, by, value):
        element = super().find_element(by, value)
        self.logger.debug("Firefox found element >>> tag: %s, location: %s",
                          element.tag_name, element.rect)
        return element

    def toJson(self):
        caps = self.capabilities
        return {
            'name': caps['browserName'],
            'version': caps['browserVersion'],
            'driver-version': caps['moz:geckodriverVersion'],
            'platform': caps['platformName']
        }


class EdgeDriver(webdriver.Edge):
    """ Custom EdgeDriver for selenium interactions."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = getLogger(__name__, self.name)

    def find_element(self, by, value):
        element = super().find_element(by, value)
        self.logger.debug("Edge found element >>> tag: %s, location: %s",
                          element.tag_name, element.rect)
        return element

    def toJson(self):
        caps = self.capabilities
        return {
            'name': caps['browserName'],
            'version': caps['browserVersion'],
            'driver-version': caps['msedge']['msedgedriverVersion'],
            'platform': caps['platformName']
        }
