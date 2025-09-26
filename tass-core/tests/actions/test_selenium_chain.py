import unittest
import pathlib
import time

import tass.core.actions.selenium_chain as chain
import selenium.webdriver.support.expected_conditions as EC
from .test_selenium import TestSelenium
from tass.core.drivers.driverconfig import new_driver
from tass.core.drivers.custombrowserdrivers import (
    FirefoxDriver as FDriver,
    SafariDriver as SDriver
)


class TestSeleniumChain(TestSelenium):

    def test_seleniumChainClickElement(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    locator = {"by": "id", "value": "btnColor"}
                    chain.click(driver, locator=locator)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[0].actions))
                    chain.perform(driver)
                    self.assertIsNotNone(driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=(
                            "xpath",
                            "//button[contains(@style, 'salmon')]"
                            )))
            finally:
                if driver:
                    driver.quit()

    def test_seleniumChainClick(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    locator = {"by": "id", "value": "btnColor"}
                    chain.move_mouse(driver, locator=locator)
                    chain.click(driver)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[0].actions))
                    chain.perform(driver)
                    self.assertIsNotNone(driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=(
                            "xpath",
                            "//button[contains(@style, 'salmon')]"
                            )))
            finally:
                if driver:
                    driver.quit()

    def test_seleniumChainReset(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    locator = {"by": "id", "value": "btnColor"}
                    chain.move_mouse(driver, locator=locator)
                    chain.click(driver)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[0].actions))
                    chain.reset(driver)
                    self.assertFalse(bool(
                        driver.chain().w3c_actions.devices[0].actions))
            finally:
                if driver:
                    driver.quit()

    def test_seleniumChainMoveTo(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    locator = {"by": "id", "value": "btn1"}
                    chain.move_mouse(driver, locator=locator)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[0].actions))
                    chain.perform(driver)
                    ele = driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=("id", "btn1"))
                    self.assertIn(
                        "0, 0, 255",
                        ele.value_of_css_property("background-color"))

            finally:
                    driver.quit()

    def test_seleniumChainScrollByAmount(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    driver().set_window_size(400, 300)
                    time.sleep(2)
                    chain.scroll(driver, deltax=0, deltay=100)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[2].actions))
                    chain.perform(driver)
                    time.sleep(2)
                    scrolled = driver() \
                        .execute_script("return window.pageYOffset")
                    self.assertGreater(scrolled, 0)
            finally:
                if driver:
                    driver.quit()

    def test_seleniumChainScrollToElement(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    if browser[1] == FDriver or browser[1] == SDriver:
                        self.skipTest(f"Not supported by {browser[1].__name__}")
                    driver().get(url)
                    driver().set_window_size(400, 300)
                    time.sleep(2)
                    locator = {"by": "id", "value": "dropdown"}
                    chain.scroll(driver, locator=locator)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[2].actions))
                    chain.perform(driver)
                    time.sleep(2)
                    # Script finds element, checks if within bounds of viewport.
                    script = (
                        "var elem = arguments[0],                 " 
                        "  box = elem.getBoundingClientRect(),    " 
                        "  cx = box.left + box.width / 2,         " 
                        "  cy = box.top + box.height / 2,         " 
                        "  e = document.elementFromPoint(cx, cy); " 
                        "for (; e; e = e.parentElement) {         " 
                        "  if (e === elem)                        " 
                        "    return true;                         " 
                        "}                                        " 
                        "return false;"
                        )
                    inView = driver() \
                        .execute_script(script, driver().find_element(**locator))
                    self.assertTrue(inView)
            finally:
                if driver:
                    driver.quit()

    def test_seleniumChainScrollFromOrigin(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    if browser[1] == FDriver or browser[1] == SDriver:
                        self.skipTest(f"Not supported by {browser[1].__name__}")
                    driver().get(url)
                    driver().set_window_size(400, 300)
                    time.sleep(2)
                    chain.scroll(driver, yoffset=0, deltax=0, deltay=600)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[2].actions))
                    chain.perform(driver)
                    time.sleep(2)
                    scrolled = driver() \
                        .execute_script("return window.pageYOffset")
                    self.assertGreater(scrolled, 0)

                    chain.reset(driver)

                    locator = {"by": "id", "value": "dropdown"}
                    chain.scroll(
                        driver,
                        locator=locator,
                        deltax=0,
                        deltay=scrolled*-1)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[2].actions))
                    chain.perform(driver)
                    time.sleep(2)
                    scrolled2 = driver() \
                        .execute_script("return window.pageYOffset")
                    self.assertEqual(scrolled2, 0)
            finally:
                if driver:
                    driver.quit()
