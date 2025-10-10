import pathlib
import tass.core.actions.selenium_wait as selwait
import selenium.webdriver.support.expected_conditions as EC
from .test_selenium import TestSelenium


class TestSeleniumWait(TestSelenium):

    def test_SeleniumWaitClickable(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = self.start_driver(browser)
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
                    locator = (
                        "xpath",
                        "//button[@id='btn-z' \
                        and contains(@style, 'salmon')]")
                    self.assertIsNotNone(driver.wait_until(
                            until_func=EC.presence_of_element_located,
                            locator=locator))
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumWaitVisible(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    driver() \
                        .find_element(*['id', 'btn-a']) \
                        .click()
                    locator = {"by": "id",
                               "value": "btn-b"}
                    selwait \
                        .wait_element_visible(driver, locator,
                                              action=['selenium', 'click'])
                    self.assertIsNotNone(driver.wait_until(
                            until_func=EC.presence_of_element_located,
                            locator=("xpath",
                                     "//button[@id='btn-b' \
                                      and contains(@style, 'salmon')]")))
            finally:
                if driver:
                    driver.quit()
