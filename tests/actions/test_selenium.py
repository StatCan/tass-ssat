import unittest
import os
import pathlib
import tass.actions.selenium as selenium
from tass.drivers.browserdriver import ChromeDriver as CDriver
from tass.drivers.browserdriver import FirefoxDriver as FDriver
from tass.drivers.browserdriver import EdgeDriver as EDriver
import selenium.webdriver.support.expected_conditions as EC


class TestSelenium(unittest.TestCase):

    config = {
            "implicit_wait": 5,
            "explicit_wait": 10,
            "options": ["--start-maximized", "--headless"]
            }

    test_page_url = 'tests/pages/page1.html'

    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        self.drivers = [EDriver, FDriver, CDriver]

    def test_SeleniumLoadURL(self):
        url = "https://www.google.ca"
        for browser in self.drivers:
            with self.subTest(browser=browser.browser):
                driver = browser(self.config)
                selenium.load_url(driver, url)
                self.assertEqual(driver.title, "Google")
                driver.quit()

    def test_SeleniumLoadFile(self):
        for browser in self.drivers:
            with self.subTest(browser=browser.browser):
                driver = browser(self.config)
                selenium.load_file(driver, self.test_page_url)
                self.assertEqual(driver.title, "Page One")
                driver.quit()

    def test_SeleniumClick(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            with self.subTest(browser=browser.browser):
                driver = browser(self.config)
                driver.get('file://' + url)
                selenium.click(driver,
                               locator={"by": "id", "value": "btnColor"})
                self.assertIsNotNone(driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=("xpath",
                                 "//button[contains(@style, 'salmon')]")))
                driver.quit()

    def test_SeleniumType(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            with self.subTest(browser=browser.browser):
                driver = browser(self.config)
                driver.get('file://' + url)
                text = 'Selenium Test Type'
                selenium.type(
                    driver, text=text,
                    locator={"by": "id", "value": "nameField"})
                self.assertEqual(
                    driver
                    .find_element('id', 'nameField')
                    .get_attribute('value'), text)
                driver.quit()

    def test_SeleniumReadAttribute(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            with self.subTest(browser=browser.browser):
                driver = browser(self.config)
                driver.get('file://' + url)
                self.assertEqual(selenium.read_attribute(
                        driver, attribute='name',
                        locator={"by": "id", "value": "btn2"}), 'button2')
                driver.quit()

    def test_SeleniumReadCSS(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            with self.subTest(browser=browser.browser):
                driver = browser(self.config)
                driver.get('file://' + url)
                self.assertEqual(selenium.read_css(
                        driver, attribute='width',
                        locator={"by": "id", "value": "btn1"}), '300px')
                driver.quit()
