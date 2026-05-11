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
import tass.core.actions.mobile.appium_wait as appwait
import selenium.webdriver.support.expected_conditions as EC
from .test_appium import TestAppium


class TestAppiumWait(TestAppium):
    btn_disabled_page = {
        "title": "Buttons | Disabled Button | QA Practice",
        "url": "https://www.qa-practice.com/elements/button/disabled",
        "page_id":
        {
            "method": "title",
            "identifier": "Buttons | Disabled Button | QA Practice"
        },
        "elements":
        {
            "hidden": {
                "by": "xpath",
                "value": "//form/input[@type='hidden']"
            },
            "btn":
            {
                "by": "xpath",
                "value": "//*[@id='submit-id-submit']"
            },
            "click-confirm":
            {
                "by": "xpath",
                "value": "//*[@id='result-text']"
            },
            "select": {
                "by": "xpath",
                "value": "//*[@id='id_select_state']"
            },
            "req-txt": {
                "by": "id",
                "value": "req_text"
            }
        }
    }

    def test_AppiumWaitClickable(self):
        url = self.btn_disabled_page['url']
        for device, driver in self.appium_starter(self.drivers):
            with self.subTest(device=device[1].__name__):
                try:
                    self.load_initial_url(driver, url)
                    self.close_nav(driver)
                    locator = self.btn_disabled_page['elements']['btn']
                    with self.assertRaises(TimeoutException):
                        appwait.wait_element_clickable(driver, locator, action=['appium', 'read_attribute'], attribute='value')
                    element = driver().find_element(**self.btn_disabled_page['elements']['select'])
                    driver.select(element, 'enabled', 'value')
                    _ = appwait.wait_element_clickable(driver, locator, action=['appium', 'read_attribute'], attribute='value')
                    self.assertIsNotNone(_)
                finally:
                    if driver:
                        driver.quit()


    def test_AppiumWaitVisible(self):
        url = self.btn_disabled_page['url']
        for device, driver in self.appium_starter(self.drivers):
            with self.subTest(device=device[1].__name__):
                try:
                    self.load_initial_url(driver, url)
                    self.close_nav(driver)
                    locator = self.btn_disabled_page['elements']['hidden']
                    with self.assertRaises(TimeoutException):
                        appwait.wait_element_visible(driver, locator, action=['appium', 'read_attribute'], attribute='value')
                    element = driver().find_element(**self.btn_disabled_page['elements']['select'])
                    driver.select(element, 'enabled', 'value')
                    driver().find_element(**self.btn_disabled_page['elements']['btn']).click()
                    self.close_nav(driver)
                    locator = self.btn_disabled_page['elements']['click-confirm']
                    _ = appwait.wait_element_clickable(driver, locator, action=['appium', 'read_attribute'], attribute='class')
                    self.assertIsNotNone(_)
                finally:
                    if driver:
                        driver.quit()
