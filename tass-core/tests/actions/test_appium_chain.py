import pathlib
import time
import tass.core.actions.mobile.appium_chain as chain
import selenium.webdriver.support.expected_conditions as EC
from .test_appium import TestAppium

class TestAppiumChain(TestAppium):

    def test_AppiumChainClickElement(self):
        url = self.pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    self.load_initial_url(driver, url)
                    self.close_nav(driver)
                    locator = self.pages['btn-page']['elements']['btn']
                    chain.click(driver, locator=locator)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[0].actions))
                    chain.perform(driver)
                    locator = ("xpath",
                               f"//*[@id='{self.pages['btn-page']['elements']['click-confirm']['value']}']")
                    self.assertIsNotNone(driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=locator
                    ))
            finally:
                if driver:
                    driver.quit()

    def test_AppiumChainWriteElement(self):
        url = self.pages['input-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    self.load_initial_url(driver, url)
                    self.close_nav(driver)
                    text = "testing"
                    locator = self.pages['input-page']['elements']['input']
                    chain.write(driver, locator=locator, text=text)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[0].actions))
                    chain.perform(driver)
                    locator = {"by": "xpath", "value": f"//*[@id='{self.pages['input-page']['elements']['input']['value']}']"}
                    actual = driver().find_element(**locator).get_attribute("value")
                    self.assertEqual(actual, text)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumChainClick(self):
        url = self.pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    self.load_initial_url(driver, url)
                    self.close_nav(driver)
                    locator = self.pages['btn-page']['elements']['btn']
                    chain.move_mouse(driver, locator=locator)
                    chain.click(driver)
                    self.assertTrue(bool(
                        driver.chain().w3c_actions.devices[0].actions))
                    chain.perform(driver)
                    locator = ("xpath",
                               f"//*[@id='{self.pages['btn-page']['elements']['click-confirm']['value']}']")
                    self.assertIsNotNone(driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=locator
                    ))
            finally:
                if driver:
                    driver.quit()

    def test_AppiumChainReset(self):
        pass

    def test_AppiumChainMoveTo(self):
        pass

    def test_AppiumChainScrollByAmount(self):
        pass

    def test_AppiumChainScrollToElement(self):
        pass

    def test_AppiumChainScrollFromOrigin(self):
        pass
