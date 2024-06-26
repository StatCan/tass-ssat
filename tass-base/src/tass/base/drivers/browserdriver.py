import ast
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from ..log.logging import getLogger


def new_driver(browser, config):
    return browser(config)


class TassDriverWrapper():
    """ Wrapper class for adding general features to browser driver classes."""
    def wait_until(self, until_func, time=None, **kwargs):
        """ Wait for element to meet condition before returning the WebElement
            This method is used to explicitly wait for a conditon to be met the
            expected condition (until_func). Once the condition is met,
            the return value of the conditonal function is returned. If
            the timeout is exceeded (configured in the 'browsers.json')
            a TimeoutException error is raised, if not configured
            the timeout defaults to 10 seconds.
        Parameters
        - - - - - - - - -
        until_func: ExpectedCondition (selenium) Function
            The conditonal function that must be met
            before a value is returned.
        **kwargs: Any type.
            Using keyword arguments to include any
            parameters required for the until_func Function.
        Returns
        - - - - - - - - -
        Any Type:
            Returns the return value of the until_func.
        """
        if (time is None):
            time = self._get_property('explicit_wait')
        wait = WebDriverWait(self, time)
        return wait.until(until_func(**kwargs))

    def _config_options(self, browser_options, options):
        options_obj = browser_options()
        # TODO: Add some default/checks in case of missing configs
        for args in options.get('arguments', []):
            options_obj.add_argument(args)
        for prefs in options.get('preferences', []):
            options_obj.set_preference(prefs[0], prefs[1])
        return options_obj

    def _implicit_wait_from_config(self):
        """ Shortcut function to set the implicit wait
            based on the configuration file.
        """
        self.implicitly_wait(self._get_property('implicit_wait'))

    def find_element(self, by, value):
        element = super().find_element(by, value)
        self.logger.debug("Found element >>> tag: %s, location: %s",
                          element.tag_name, element.rect)
        return element


class ChromeDriver(TassDriverWrapper, webdriver.Chrome):
    """ Custom ChromeDriver for selenium interactions."""
    def __init__(self, config):
        self.logger = getLogger(__name__, 'chrome')
        self._config = config
        super().__init__(options=self._config_options(
                                    webdriver.ChromeOptions,
                                    self._get_property('options')))
        self._implicit_wait_from_config()

    def toJson(self):
        # TODO: Include configuration information in the output.
        caps = self.capabilities
        return {
            'name': caps['browserName'],
            'version': caps['browserVersion'],
            'driver-version': caps['chrome']['chromedriverVersion'],
            'platform': caps['platformName']
        }

    def _get_property(self, prop):
        return ast.literal_eval(self._config.get('chrome', prop))


class FirefoxDriver(TassDriverWrapper, webdriver.Firefox):
    """ Custom FirefoxDriver for selenium interactions."""
    def __init__(self, config):
        self.logger = getLogger(__name__, 'firefox')
        self._config = config
        super().__init__(options=self._config_options(
                                    webdriver.FirefoxOptions,
                                    self._get_property('options')))
        self._implicit_wait_from_config()
        if ('--start-maximized' in self._get_property('options')):
            self.maximize_window()

    def toJson(self):
        # TODO: Include configuration information in the output.
        caps = self.capabilities
        return {
            'name': caps['browserName'],
            'version': caps['browserVersion'],
            'driver-version': caps['moz:geckodriverVersion'],
            'platform': caps['platformName']
        }

    def _get_property(self, prop):
        return ast.literal_eval(self._config.get('firefox', prop))


class EdgeDriver(TassDriverWrapper, webdriver.Edge):
    """ Custom EdgeDriver for selenium interactions."""
    def __init__(self, config):
        self.logger = getLogger(__name__, 'edge')
        self._config = config
        super().__init__(options=self._config_options(
                            webdriver.EdgeOptions,
                            self._get_property('options')))
        self._implicit_wait_from_config()

    def toJson(self):
        # TODO: Include configuration information in the output.
        caps = self.capabilities
        return {
            'name': caps['browserName'],
            'version': caps['browserVersion'],
            'driver-version': caps['msedge']['msedgedriverVersion'],
            'platform': caps['platformName']
        }

    def _get_property(self, prop):
        return ast.literal_eval(self._config.get('edge', prop))
