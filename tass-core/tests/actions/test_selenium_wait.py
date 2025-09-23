import unittest
import pathlib

import tass.core.actions.selenium_wait as selwait
import selenium.webdriver.support.expected_conditions as EC
from .test_selenium import TestSelenium
from tass.core.drivers.driverconfig import new_driver
from tass.core.drivers.custombrowserdrivers import (
    ChromeDriver as CDriver,
    EdgeDriver as EDriver,
    FirefoxDriver as FDriver
)


class TestSeleniumWait(TestSelenium):

    def test_SeleniumWaitClickable(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = new_driver(**browser[0])
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    driver() \
                        .find_element(*['id', 'btn-y']) \
                        .click()
                    selwait \
                        .wait_element_clickable(driver,
                                                {
                                                    "by": "id",
                                                    "value":
                                                    "btn-z"
                                                },
                                                action=['selenium', 'click'])
                    self.assertIsNotNone(driver.wait_until(
                            until_func=EC.presence_of_element_located,
                            locator=("xpath",
                                    "//button[@id='btn-z' \
                                    and contains(@style, 'salmon')]")))
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumWaitVisible(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = new_driver(**browser[0])
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    driver() \
                        .find_element(*['id', 'btn-a']) \
                        .click()
                    selwait \
                        .wait_element_visible(driver,
                                            {
                                                "by": "id",
                                                "value":
                                                "btn-b"
                                            },
                                            action=['selenium', 'click'])
                    self.assertIsNotNone(driver.wait_until(
                            until_func=EC.presence_of_element_located,
                            locator=("xpath",
                                    "//button[@id='btn-b' \
                                    and contains(@style, 'salmon')]")))
            finally:
                if driver:
                    driver.quit()
