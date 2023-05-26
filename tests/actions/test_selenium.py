import unittest
import os
import pathlib
import tass.actions.selenium as selenium
from tass.drivers.browserdriver import ChromeDriver as CDriver
from tass.drivers.browserdriver import FirefoxDriver as FDriver
from tass.drivers.browserdriver import EdgeDriver as EDriver
from tass.exceptions.assertion_errors import TassAssertionError
from tass.exceptions.assertion_errors import TassHardAssertionError
from tass.exceptions.assertion_errors import TassSoftAssertionError
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

        self.drivers = [CDriver, EDriver, FDriver]

    def test_SeleniumLoadURL(self):
        url = "https://www.google.ca"
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                selenium.load_url(driver, url)
                self.assertEqual(driver.title, "Google")
                driver.quit()

    def test_SeleniumLoadFile(self):
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                selenium.load_file(driver, self.test_page_url)
                self.assertEqual(driver.title, "Page One")
                driver.quit()

    def test_SeleniumClick(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                selenium.click(driver,
                               locator={"by": "id", "value": "btnColor"})
                self.assertIsNotNone(driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=("xpath",
                                 "//button[contains(@style, 'salmon')]")))
                driver.quit()

    def test_SeleniumWrite(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                text = 'Selenium Test Type'
                selenium.write(
                    driver, text=text,
                    locator={"by": "id", "value": "nameField"})
                self.assertEqual(
                    driver
                    .find_element('id', 'nameField')
                    .get_attribute('value'), text)
                driver.quit()

    def test_SeleniumClear(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                text = 'Selenium Test Type'
                driver.find_element('id', 'nameField').send_keys(text)
                self.assertEqual(
                    driver
                    .find_element('id', 'nameField')
                    .get_attribute('value'), text)
                selenium.clear(
                    driver,
                    locator={"by": "id", "value": "nameField"})
                self.assertEqual(
                    driver
                    .find_element('id', 'nameField')
                    .get_attribute('value'), '')
                driver.quit()

    def test_SeleniumReadAttribute(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                self.assertEqual(selenium.read_attribute(
                        driver, attribute='name',
                        locator={"by": "id", "value": "btn2"}), 'button2')
                driver.quit()

    def test_SeleniumReadCSS(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                self.assertEqual(selenium.read_css(
                        driver, attribute='width',
                        locator={"by": "id", "value": "btn1"}), '300px')
                driver.quit()

    def test_SeleniumAssertDisplayedSuccess(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                try:
                    selenium.assert_displayed(
                        driver,
                        locator={"by": "id", "value": "btn1"})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertDisplayedFailed(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                with self.assertRaises(TassHardAssertionError):
                    selenium.assert_displayed(
                        driver,
                        locator={"by": "id", "value": "btn-x"})

                driver.quit()

    def test_SeleniumAssertDisplayedSoftSuccess(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                try:
                    selenium.assert_displayed(
                        driver, soft=True,
                        locator={"by": "id", "value": "btn1"})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertDisplayedSoftFailed(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                with self.assertRaises(TassSoftAssertionError):
                    selenium.assert_displayed(
                        driver, soft=True,
                        locator={"by": "id", "value": "btn-x"})

                driver.quit()

    def test_SeleniumAssertNotDisplayedSuccess(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                try:
                    selenium.assert_not_displayed(
                        driver,
                        locator={"by": "id", "value": "btn-x"})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertNotDisplayedFailed(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                with self.assertRaises(TassHardAssertionError):
                    selenium.assert_not_displayed(
                        driver,
                        locator={"by": "id", "value": "btn1"})

                driver.quit()

    def test_SeleniumAssertNotDisplayedSoftSuccess(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                try:
                    selenium.assert_not_displayed(
                        driver, soft=True,
                        locator={"by": "id", "value": "btn-x"})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertNotDisplayedSoftFailed(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                with self.assertRaises(TassSoftAssertionError):
                    selenium.assert_not_displayed(
                        driver, soft=True,
                        locator={"by": "id", "value": "btn1"})

                driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleSoftFailure(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                with self.assertRaises(TassSoftAssertionError):
                    selenium.assert_page_is_open(
                        driver, soft=True, page_id={
                                                    'identifier': 'Page One1',
                                                    'method': 'title'})

                driver.quit()

    def test_SeleniumAssertPageIsOpenByURLSoftFailure(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                with self.assertRaises(TassSoftAssertionError):
                    selenium.assert_page_is_open(
                        driver, soft=True, page_id={
                                                'identifier': 'not the url',
                                                'method': 'url'})

                driver.quit()

    def test_SeleniumAssertPageIsOpenByElementSoftFailure(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                with self.assertRaises(TassSoftAssertionError):
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': {
                                        'locator': {
                                            'by': 'id',
                                            'value': 'noElement'
                                            }
                                        },
                                    'method': 'element'
                                    },
                        soft=True)

                driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleSoftSuccess(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                try:
                    selenium.assert_page_is_open(
                        driver, soft=True, page_id={
                                                    'identifier': 'Page One',
                                                    'method': 'title'})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertPageIsOpenByURLSoftSuccess(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                try:
                    selenium.assert_page_is_open(
                        driver, soft=True, page_id={
                                                'identifier': 'file://' + url,
                                                'method': 'url'})
                except TassAssertionError as e:
                    self.fail(e.message)

                driver.quit()

    def test_SeleniumAssertPageIsOpenByElementSoftSuccess(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                try:
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': {
                                        'locator': {
                                            'by': 'id',
                                            'value': 'btnColor'
                                            }
                                        },
                                    'method': 'element'
                                    },
                        soft=True)
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleFailure(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                with self.assertRaises(TassHardAssertionError):
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': 'Page One1',
                                    'method': 'title'})

                driver.quit()

    def test_SeleniumAssertPageIsOpenByURLFailure(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                with self.assertRaises(TassHardAssertionError):
                    selenium.assert_page_is_open(
                        driver, 'not the url', page_id={
                                                'identifier': 'not the url',
                                                'method': 'url'})

                driver.quit()

    def test_SeleniumAssertPageIsOpenByElementFailure(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                with self.assertRaises(TassHardAssertionError):
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': {
                                        'locator': {
                                            'by': 'id',
                                            'value': 'noElement'
                                            }
                                        },
                                    'method': 'element'
                                    })

                driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleSuccess(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                try:
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': 'Page One',
                                    'method': 'title'})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertPageIsOpenByURLSuccess(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                try:
                    selenium.assert_page_is_open(
                        driver, 'file://' + url, page_id={
                                                'identifier': 'file://' + url,
                                                'method': 'url'})
                except TassAssertionError as e:
                    self.fail(e.message)

                driver.quit()

    def test_SeleniumAssertPageIsOpenByElementSuccess(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get('file://' + url)
                try:
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': {
                                        'locator': {
                                            'by': 'id',
                                            'value': 'btnColor'
                                            }
                                        },
                                    'method': 'element'
                                    })
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumSwitchWindowNoTitle(self):
        url_0 = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        url_1 = 'https://www.google.ca'
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url_1)
                driver.switch_to.new_window('tab')
                driver.get('file://' + url_0)
                self.assertEqual(driver.title, 'Page One')
                selenium.switch_window(driver)
                self.assertEqual(driver.title, 'Google')

            driver.quit()

    def test_SeleniumSwitchWindowByTitle(self):
        url_0 = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        url_1 = 'https://www.google.ca'
        url_2 = 'https://www.github.com'
        google = 'Google'
        pageOne = 'Page One'
        github = 'GitHub: Let’s build from here · GitHub'
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url_1)
                driver.switch_to.new_window('tab')
                driver.get(url_2)
                driver.switch_to.new_window('tab')
                driver.get('file://' + url_0)
                self.assertEqual(driver.title, pageOne)
                selenium.switch_window(driver, google)
                self.assertEqual(driver.title, google)
                selenium.switch_window(driver, github)
                self.assertEqual(driver.title, github)
                selenium.switch_window(driver, pageOne)
                self.assertEqual(driver.title, pageOne)

            driver.quit()
