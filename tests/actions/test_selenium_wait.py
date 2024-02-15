import unittest
import pathlib
import tass.actions.selenium_wait as selwait
import tass.config.browserconfig as bc
from tass.drivers.browserdriver import ChromeDriver as CDriver
from tass.drivers.browserdriver import FirefoxDriver as FDriver
from tass.drivers.browserdriver import EdgeDriver as EDriver
import selenium.webdriver.support.expected_conditions as EC


class TestSeleniumWait(unittest.TestCase):

    config = bc.load(
        {
            "DEFAULT": {
                "implicit_wait": 5,
                "explicit_wait": 10,
                "options": {
                    "arguments": ["--start-maximized", "--headless"],
                    "preferences": []
                    }
                },
            "firefox": {
                "name": "firefox",
                "options": {
                    "arguments": ["--start-maximized", "--headless"],
                    "preferences":
                        [
                            ["app.update.auto", False],
                            ["app.update.enabled", False]
                        ]
                    }
                }
        })

    test_page_url = 'tests/pages/page1.html'

    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        self.drivers = [CDriver, EDriver, FDriver]

    def test_SeleniumWaitClickable(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                driver \
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
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                driver \
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
