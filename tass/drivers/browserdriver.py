from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def newDriver(browser, config):
    return browser(config)


class WebDriverWaitWrapper():
    """ Wrapper class for adding general features to browser driver classes."""
    def wait_until(self, until_func, **kwargs):
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
        wait = WebDriverWait(self, self._config.get('explicit_wait', 10))
        return wait.until(until_func(**kwargs))

    def _config_options(self, browser_options, config):
        options_obj = browser_options()
        for opt in config.get('options', []):
            options_obj.add_argument(opt)
        return options_obj

    def _implicit_wait_from_config(self):
        """ Shortcut function to set the implicit wait
            based on the configuration file.
        """
        self.implicitly_wait(self._config.get('implicit_wait', 10))


class ChromeDriver(webdriver.Chrome, WebDriverWaitWrapper):
    browser = 'Chrome'
    """ Custom ChromeDriver for selenium interactions."""
    def __init__(self, config):
        self._config = config
        super().__init__(service=ChromeService(
            ChromeDriverManager().install()),
            options=self._config_options(webdriver.ChromeOptions, config))
        self._implicit_wait_from_config()


class FirefoxDriver(webdriver.Firefox, WebDriverWaitWrapper):
    browser = 'Firefox'
    """ Custom FirefoxDriver for selenium interactions."""
    def __init__(self, config):
        self._config = config
        super().__init__(service=FirefoxService(
            GeckoDriverManager().install()),
            options=self._config_options(webdriver.FirefoxOptions, config))
        self._implicit_wait_from_config()
        if ('--start-maximized' in config.get('options', [])):
            self.maximize_window()


class EdgeDriver(webdriver.Edge, WebDriverWaitWrapper):
    browser = 'Edge'
    """ Custom EdgeDriver for selenium interactions."""
    def __init__(self, config):
        self._config = config
        super().__init__(service=EdgeService(
            EdgeChromiumDriverManager().install()),
            options=self._config_options(webdriver.EdgeOptions, config))
        self._implicit_wait_from_config()
