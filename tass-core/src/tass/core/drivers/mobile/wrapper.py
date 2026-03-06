from enum import Enum
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from appium.options.common import AppiumOptions
from . import scripting
from ...log.logging import getLogger
from ..wrapper import BaseDriverWrapper
from .appium_service import TASSAppiumService
from .customdrivers import TassMobileDriverWait
from .customdrivers import (
    AndroidDriver,
    IOSDriver
    )


log = getLogger(__name__)


class BaseMobileDriverWrapper(BaseDriverWrapper):

    executor = scripting.MobileDriverScriptExecutor

    def __init__(self, uuid, configs, *args, **kwargs):
        super().__init__(uuid, configs, *args, **kwargs)
        self._service = None

    def __call__(self, driver_options, driver_init, *args, **kwargs):
        if not self._driver:
            options = self.set_options(driver_options)
            # Start Appium Service
            self._service = TASSAppiumService.service(self,
                                                      self._conf["appium:server"]
            )
            TASSAppiumService.start_service(self._service)
            # run before scripts
            if "setup" in self._conf:
                for func in self._conf["setup"]:
                    _ = self.executor.execute(func, driver_wrapper=self) or "Completed"
                    log.debug("Setup script result: %s", _)
            # initialize driver
            self._driver = driver_init(options=options, *args, **kwargs)

            # set driver settings
            self._driver.implicitly_wait(
                self._conf['driver'].get('implicit_wait', 5)
                )

        return self._with_delay(self._driver)

    @property
    def uuid(self):
        return self._uuid

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
            return self._driver.capabilities.get("platformName", None)
        return None
    
    @property
    def device_id(self):
        # extract device id from driver
        if self._driver:
            return self._driver.capabilities.get("udid", None)
        # extract device id from configs if driver not instantiated
        elif "udid" in self._conf["appium:driver"]:
            return self._conf["appium:driver"]["udid"]
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

        configs.setdefault('appium:driver', {})
        for k, v in self.DEFAULT_CAPS.items():
            configs['appium:driver'].setdefault(k, v)
        configs.setdefault('appium:server', {})

        return configs

    def set_options(self, browser_options):
        options = browser_options()
        caps = {}
        caps.update(self.DEFAULT_CAPS)
        caps.update(self._conf["appium:driver"])
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

    def select(self, element, value, using):
        # send_keys to scroll element into view.
        element.send_keys("")
        match using:
            case 'text':
                select = Select(element).select_by_visible_text
                value = str(value)
                log.debug('Selecting with visible text')
            case 'value':
                select = Select(element).select_by_value
                value = str(value)
                log.debug('Selecting using option value')
            case 'index':
                select = Select(element).select_by_index
                value = int(value)
                log.debug("Selecting using option index")
            case _:
                raise ValueError(f'Select method {using} is not a valid method.')
        select(value)

    def quit(self):
        # Execute teardown scripts if any
        if "teardown" in self._conf:
            for func in self._conf["teardown"]:
                _ = self.executor.execute(func, driver_wrapper=self) or "Completed"
                log.debug("Teardown script result: %s", _)
        if self._driver:
            self._driver.quit()
        if self._service:
            TASSAppiumService.stop_service(self._service)
        self._waits = {}
        self._chain = None
        self._driver = None
        self._service = None


class AndroidDriverWrapper(BaseMobileDriverWrapper):
    DEFAULT_CAPS = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
    }

    executor = scripting.AndroidDriverScriptExecutor
    def __init__(self, uuid, configs,
                 *args, **kwargs):
        super().__init__(uuid, configs, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(AppiumOptions, AndroidDriver, *args, **kwargs)

    def quit(self):
        if self._driver:
            self._driver.terminate_app("com.android.chrome")
        super().quit()


class IOSDriverWrapper(BaseMobileDriverWrapper):
    DEFAULT_CAPS = {
        "platformName": "ios",
        "automationName": "xcuitest",
    }

    executor = scripting.IOSDriverScriptExecutor
    def __init__(self, uuid, configs,
                 *args, **kwargs):
        super().__init__(uuid, configs, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(AppiumOptions, IOSDriver, *args, **kwargs)
