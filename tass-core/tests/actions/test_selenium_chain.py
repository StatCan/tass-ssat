import unittest
import pathlib

import tass.core.actions.selenium_chain as chain
import selenium.webdriver.support.expected_conditions as EC

from tass.core.drivers.driverconfig import new_driver
from tass.core.drivers.custombrowserdrivers import (
    ChromeDriver as CDriver,
    EdgeDriver as EDriver,
    FirefoxDriver as FDriver
)


class TestSeleniumChain(unittest.TestCase):
        
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

            self.drivers = [(self.config[0], CDriver),
                            (self.config[1], FDriver),
                            (self.config[2], EDriver)]

        def test_seleniumChainClickElement(self):
            url = pathlib.Path(self.test_page_url).resolve().as_uri()
            for browser in self.drivers:
                driver = new_driver(**browser[0])
                with self.subTest(browser=browser[1].__name__):
                     driver().get(url)
                     locator = {"by": "id", "value": "btnColor"}
                     chain.click(driver, locator=locator)
                     self.assertTrue(bool(driver.chain().w3c_actions.devices[0].actions))
                     chain.perform(driver)
                     self.assertIsNotNone(driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=("xpath",
                                 "//button[contains(@style, 'salmon')]")))
                     driver.quit()

        def test_seleniumChainClick(self):
            url = pathlib.Path(self.test_page_url).resolve().as_uri()
            for browser in self.drivers:
                driver = new_driver(**browser[0])
                with self.subTest(browser=browser[1].__name__):
                     driver().get(url)
                     locator = {"by": "id", "value": "btnColor"}
                     chain.move_mouse(driver, locator=locator)
                     chain.click(driver)
                     self.assertTrue(bool(driver.chain().w3c_actions.devices[0].actions))
                     chain.perform(driver)
                     self.assertIsNotNone(driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=("xpath",
                                 "//button[contains(@style, 'salmon')]")))
                     driver.quit()

        def test_seleniumChainReset(self):
            url = pathlib.Path(self.test_page_url).resolve().as_uri()
            for browser in self.drivers:
                driver = new_driver(**browser[0])
                with self.subTest(browser=browser[1].__name__):
                     driver().get(url)
                     locator = {"by": "id", "value": "btnColor"}
                     chain.move_mouse(driver, locator=locator)
                     chain.click(driver)
                     self.assertTrue(bool(driver.chain().w3c_actions.devices[0].actions))
                     chain.reset(driver)
                     self.assertFalse(bool(driver.chain().w3c_actions.devices[0].actions))
                     driver.quit()

        def test_seleniumChainMoveTo(self):
            url = pathlib.Path(self.test_page_url).resolve().as_uri()
            for browser in self.drivers:
                driver = new_driver(**browser[0])
                with self.subTest(browser=browser[1].__name__):
                     driver().get(url)
                     locator = {"by": "id", "value": "btn1"}
                     chain.move_mouse(driver, locator=locator)
                     self.assertTrue(bool(driver.chain().w3c_actions.devices[0].actions))
                     chain.perform(driver)
                     ele = driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=("id", "btn1"))
                     self.assertIn("0, 0, 255", ele.value_of_css_property("background-color"))
                     
                     driver.quit()