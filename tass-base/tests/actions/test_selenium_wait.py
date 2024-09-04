import unittest
import pathlib

import tass.base.actions.selenium_wait as selwait
import selenium.webdriver.support.expected_conditions as EC
from tass.base.drivers.driverconfig import new_driver
from tass.base.drivers.custombrowserdrivers import (
    ChromeDriver as CDriver,
    EdgeDriver as EDriver,
    FirefoxDriver as FDriver
)


class TestSeleniumWait(unittest.TestCase):

    config = [
        {
            "browser_name": "chrome",
            "uuid": "chromeTEST",
            "configs": {
                "driver": {
                    "implicit_wait": "5",
                    "explicit_wait": "20"
                },
                "browser": {
                    "arguments": [
                        "--start-maximized",
                        "--headless"
                    ],
                    "preferences": {}
                }
            }
        },
        {
            "browser_name": "firefox",
            "uuid": "firefoxTEST",
            "configs": {
                "driver": {
                    "implicit_wait": "5",
                    "explicit_wait": "20"
                },
                "browser": {
                    "arguments": [
                        "--start-maximized",
                        "--headless"
                    ],
                    "preferences": {}
                }
            }
        },
        {
            "browser_name": "edge",
            "uuid": "edgeTEST",
            "configs": {
                "driver": {
                    "implicit_wait": "5",
                    "explicit_wait": "20"
                },
                "browser": {
                    "arguments": [
                        "--start-maximized",
                        "--headless"
                    ],
                    "preferences": {}
                }
            }
        }
    ]

    test_page_url = (
        str(pathlib.Path(__file__).parents[1].resolve())
        + '/pages/page1.html'
        )

    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        self.drivers = [(self.config[0], CDriver), (self.config[1], FDriver), (self.config[2], EDriver)]

    def test_SeleniumWaitClickable(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
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
                driver.quit()

    def test_SeleniumWaitVisible(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
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
                driver.quit()
