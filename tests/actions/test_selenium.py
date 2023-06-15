import unittest
import pathlib
import tass.actions.selenium as selenium
from tass.drivers.browserdriver import ChromeDriver as CDriver
from tass.drivers.browserdriver import FirefoxDriver as FDriver
from tass.drivers.browserdriver import EdgeDriver as EDriver
from tass.exceptions.assertion_errors import TassAssertionError
from tass.exceptions.assertion_errors import TassHardAssertionError
from tass.exceptions.assertion_errors import TassSoftAssertionError
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.select import Select


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
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                selenium.click(driver,
                               locator={"by": "id", "value": "btnColor"})
                self.assertIsNotNone(driver.wait_until(
                        until_func=EC.presence_of_element_located,
                        locator=("xpath",
                                 "//button[contains(@style, 'salmon')]")))
                driver.quit()

    def test_SeleniumWrite(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
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
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
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
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                self.assertEqual(selenium.read_attribute(
                        driver, attribute='name',
                        locator={"by": "id", "value": "btn2"}), 'button2')
                driver.quit()

    def test_SeleniumReadCSS(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                self.assertEqual(selenium.read_css(
                        driver, attribute='width',
                        locator={"by": "id", "value": "btn1"}), '300px')
                driver.quit()

    def test_SeleniumSwitchToFrameId(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                selenium.switch_frame(driver, frame='FrameA')
                btnName = driver.find_element(
                    *('id', 'btnColor')).get_attribute('name')
                self.assertEqual(btnName, 'buttonAlpha')
                driver.quit()

    def test_SeleniumSwitchToFrameElement(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                selenium.switch_frame(driver, frame={
                                    'locator': {
                                        'by': 'xpath',
                                        'value': '//iframe[@title="Iframe 2"]'
                                    }})
                btnName = driver.find_element(
                    *('id', 'btnColor')).get_attribute('name')
                self.assertEqual(btnName, 'buttonAlpha')
                driver.quit()

    def test_SeleniumSelectDropdownByText(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                selenium.select_dropdown(driver, 'AA', 'text',
                                         locator={
                                            'by': 'id', 'value': 'dropdown'
                                            })
                sel = Select(driver.find_element('id', 'dropdown'))
                self.assertEqual(sel.first_selected_option.text, 'AA')
                driver.quit()

    def test_SeleniumSelectDropdownByValue(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                selenium.select_dropdown(driver, 'last', 'value',
                                         locator={
                                            'by': 'id', 'value': 'dropdown'
                                            })
                sel = Select(driver.find_element('id', 'dropdown'))
                self.assertEqual(sel.first_selected_option.text, 'AA')
                driver.quit()

    def test_SeleniumSelectDropdownByIndex(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                selenium.select_dropdown(driver, 3, 'index',
                                         locator={
                                            'by': 'id', 'value': 'dropdown'
                                            })
                sel = Select(driver.find_element('id', 'dropdown'))
                self.assertEqual(sel.first_selected_option.text, 'AA')
                driver.quit()

    def test_SeleniumAssertDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                try:
                    selenium.assert_displayed(
                        driver,
                        locator={"by": "id", "value": "btn1"})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertDisplayedFailed(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                with self.assertRaises(TassHardAssertionError):
                    selenium.assert_displayed(
                        driver,
                        locator={"by": "id", "value": "btn-x"})

                driver.quit()

    def test_SeleniumAssertDisplayedSoftSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                try:
                    selenium.assert_displayed(
                        driver, soft=True,
                        locator={"by": "id", "value": "btn1"})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertDisplayedSoftFailed(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                with self.assertRaises(TassSoftAssertionError):
                    selenium.assert_displayed(
                        driver, soft=True,
                        locator={"by": "id", "value": "btn-x"})

                driver.quit()

    def test_SeleniumAssertNotDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                try:
                    selenium.assert_not_displayed(
                        driver,
                        locator={"by": "id", "value": "btn-x"})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertNotDisplayedFailed(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                with self.assertRaises(TassHardAssertionError):
                    selenium.assert_not_displayed(
                        driver,
                        locator={"by": "id", "value": "btn1"})

                driver.quit()

    def test_SeleniumAssertNotDisplayedSoftSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                try:
                    selenium.assert_not_displayed(
                        driver, soft=True,
                        locator={"by": "id", "value": "btn-x"})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertNotDisplayedSoftFailed(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                with self.assertRaises(TassSoftAssertionError):
                    selenium.assert_not_displayed(
                        driver, soft=True,
                        locator={"by": "id", "value": "btn1"})

                driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                with self.assertRaises(TassSoftAssertionError):
                    selenium.assert_page_is_open(
                        driver, soft=True, page_id={
                                                    'identifier': 'Page One1',
                                                    'method': 'title'})

                driver.quit()

    def test_SeleniumAssertPageIsOpenByURLSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                with self.assertRaises(TassSoftAssertionError):
                    selenium.assert_page_is_open(
                        driver, soft=True, page_id={
                                                'identifier': 'not the url',
                                                'method': 'url'})

                driver.quit()

    def test_SeleniumAssertPageIsOpenByElementSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                with self.assertRaises(TassSoftAssertionError):
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': {
                                        'by': 'id',
                                        'value': 'noElement'
                                        },
                                    'method': 'element'
                                    },
                        soft=True)

                driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleSoftSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                try:
                    selenium.assert_page_is_open(
                        driver, soft=True, page_id={
                                                    'identifier': 'Page One',
                                                    'method': 'title'})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertPageIsOpenByURLSoftSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                try:
                    selenium.assert_page_is_open(
                        driver, soft=True, page_id={
                                                'identifier': url,
                                                'method': 'url'})
                except TassAssertionError as e:
                    self.fail(e.message)

                driver.quit()

    def test_SeleniumAssertPageIsOpenByElementSoftSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                try:
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': {
                                        'by': 'id',
                                        'value': 'btnColor'
                                        },
                                    'method': 'element'
                                    },
                        soft=True)
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                with self.assertRaises(TassHardAssertionError):
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': 'Page One1',
                                    'method': 'title'})

                driver.quit()

    def test_SeleniumAssertPageIsOpenByURLFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                with self.assertRaises(TassHardAssertionError):
                    selenium.assert_page_is_open(
                        driver, page_id={
                                                'identifier': 'not the url',
                                                'method': 'url'})

                driver.quit()

    def test_SeleniumAssertPageIsOpenByElementFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                with self.assertRaises(TassHardAssertionError):
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': {
                                        'by': 'id',
                                        'value': 'noElement'
                                        },
                                    'method': 'element'
                                    })

                driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                try:
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': 'Page One',
                                    'method': 'title'})
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumAssertPageIsOpenByURLSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                try:
                    selenium.assert_page_is_open(
                        driver, page_id={
                                                'identifier': url,
                                                'method': 'url'})
                except TassAssertionError as e:
                    self.fail(e.message)

                driver.quit()

    def test_SeleniumAssertPageIsOpenByElementSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url)
                try:
                    selenium.assert_page_is_open(
                        driver, page_id={
                                    'identifier': {
                                        'by': 'id',
                                        'value': 'btnColor'
                                        },
                                    'method': 'element'
                                    })
                except TassAssertionError as e:
                    self.fail(e.message)
                driver.quit()

    def test_SeleniumSwitchWindowNoTitle(self):
        url_0 = pathlib.Path(self.test_page_url).resolve().as_uri()
        url_1 = 'https://www.google.ca'
        for browser in self.drivers:
            driver = browser(self.config)
            with self.subTest(browser=driver.toJson()):
                driver.get(url_1)
                driver.switch_to.new_window('tab')
                driver.get(url_0)
                self.assertEqual(driver.title, 'Page One')
                selenium.switch_window(driver)
                self.assertEqual(driver.title, 'Google')

            driver.quit()

    def test_SeleniumSwitchWindowByTitle(self):
        url_0 = pathlib.Path(self.test_page_url).resolve().as_uri()
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
                driver.get(url_0)
                self.assertEqual(driver.title, pageOne)
                selenium.switch_window(driver, google)
                self.assertEqual(driver.title, google)
                selenium.switch_window(driver, github)
                self.assertEqual(driver.title, github)
                selenium.switch_window(driver, pageOne)
                self.assertEqual(driver.title, pageOne)

            driver.quit()
