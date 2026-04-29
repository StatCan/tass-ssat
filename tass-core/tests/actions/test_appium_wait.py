import unittest
import importlib
import pathlib
import time
from sys import platform
from tass.core.drivers.new_driver import new_driver
from tass.core.tools.page_reader import PageReader
from tass.core.exceptions.assertion_errors import (
    TassAssertionError,
    TassHardAssertionError,
    TassSoftAssertionError)
from selenium.common.exceptions import (NoSuchElementException, TimeoutException)
from selenium.webdriver.support.select import Select
import tass.core.actions.mobile.appium as appium
import selenium.webdriver.support.expected_conditions as EC
from .test_appium import TestAppium


class TestAppiumWait(TestAppium):

    def test_AppiumWaitClickable(self):
        pass

    def test_AppiumWaitVisible(self):
        pass
