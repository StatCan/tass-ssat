from enum import Enum
from selenium.webdriver.common.action_chains import ActionChains
from appium.options.common import AppiumOptions
from ...log.logging import getLogger
from .customdrivers import TassMobileDriverWait
from .customdrivers import (
    AndroidDriver,
    IOSDriver
    )


log = getLogger(__name__)


def new_driver(uuid, browser_name, configs):
    log.info("Creating driver for: %s", browser_name)
    try:
        wrapper = SupportedBrowsers[browser_name.upper()].value
    except KeyError:
        log.warning("%s browser not supported.", browser_name)
        return None

    return wrapper(uuid, configs)


class BaseMobileDriverWrapper():
    def __init__(self, uuid, configs):
        self._waits = {}
        self._conf = self._set_defaults(configs)
        self._driver = None
        self._uuid = uuid
        self._chain = None

    def __call__(self, driver_options, driver_init, *args, **kwargs):
        if not self._driver:
            options = self.set_options(driver_options)
            self._driver = driver_init(options=options, *args, **kwargs)

            # set driver settings
            self._driver.implicitly_wait(
                self._conf['driver'].get('implicit_wait', 5)
                )
        return self._driver

    @property
    def browser(self):
        if (self._driver):
            return self._driver.capabilities.get("browserName", None)
        return None

    @property
    def name(self):
        if (self._driver):
            return self._driver.capabilities.get("automationName", None)
        return None

    @property
    def browser_version(self):
        if (self._driver):
            return self._driver.capabilities.get("browserVersion", None)
        return None

    @property
    def os(self):
        if (self._driver):
            return self._driver.capabilities["platformName"]
        return None

    def _set_defaults(self, configs):
        # set default values for driver settings
        configs.setdefault('driver', {})
        configs['driver'].setdefault('implicit_wait', 5)
        configs['driver'].setdefault('explicit_wait', 20)

        # set default values for brower settings
        configs.setdefault('browser', {})
        configs['browser'].setdefault('preferences', [])
        configs['browser'].setdefault('arguments', [])

        configs.setdefault('appium', self.DEFAULT_CAPS)

        return configs

    def set_options(self, browser_options):
        options = browser_options()
        caps = {}
        caps.update(self.DEFAULT_CAPS)
        caps.update(self._conf["appium"])
        options.load_capabilities(caps)
        conf = self._conf['browser']

        # get browser preferences
        for prefs in conf.get('preferences', []):
            options.set_preference(prefs[0], prefs[1])

        # get browser arguments/flags
        for args in conf.get('arguments', []):
            options.add_argument(args)

        return options

    def chain(self):
        if not self._chain:
            self._chain = ActionChains(self())
        return self._chain

    def wait_until(self, until_func, time=None,
                   poll_frequency=0,
                   ignored_exceptions=None,
                   **kwargs):
        def new_wait(time):
            wait_ = TassMobileDriverWait(self(), time,
                                   poll_frequency,
                                   ignored_exceptions)
            self._waits[time] = wait_
            return wait_
        if not time:
            time = self._conf['driver'].get('explicit_wait', 20)

        wait_ = self._waits.get(time, new_wait(time))
        return wait_.until(until_func(**kwargs))

    def quit(self):
        if self._chain:
            self._chain.reset_actions()
        if self._driver:
            self._driver.quit()
        self._waits = {}
        self._chain = None
        self._driver = None


class AndroidDriverWrapper(BaseMobileDriverWrapper):
    DEFAULT_CAPS = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
    }
    def __init__(self, uuid, configs,
                 *args, **kwargs):
        super().__init__(uuid, configs, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(AppiumOptions, AndroidDriver, *args, **kwargs)


class IOSDriverWrapper(BaseMobileDriverWrapper):
    DEFAULT_CAPS = {
        "platformName": "ios",
        "automationName": "xcuitest",
    }
    def __init__(self, uuid, configs,
                 *args, **kwargs):
        super().__init__(uuid, configs, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(AppiumOptions, IOSDriver, *args, **kwargs)
