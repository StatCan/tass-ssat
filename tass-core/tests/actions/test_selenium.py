import unittest
import pathlib
from sys import platform

import tass.core.actions.selenium as selenium
from tass.core.tools.page_reader import PageReader
from tass.core.exceptions.assertion_errors import (
    TassAssertionError,
    TassHardAssertionError,
    TassSoftAssertionError
)

import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.select import Select
from tass.core.drivers.new_driver import new_driver
from tass.core.drivers.browser.customdrivers import (
    ChromeDriver as CDriver,
    EdgeDriver as EDriver,
    FirefoxDriver as FDriver,
    SafariDriver as SDriver
)


class TestSelenium(unittest.TestCase):

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
        },
        {
            "browser_name": "safari",
            "uuid": "safariTEST",
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
        if platform == "darwin":
            self.drivers.append((self.config[3], SDriver))

    def start_driver(self, browser):
        print("\nStarting driver for: %s" % browser[1].__name__)
        return new_driver(**browser[0])


class TestSeleniumStartupActions(TestSelenium):

    def test_SeleniumNewDriver(self):
        for browser in self.drivers:
            with self.subTest(browser=browser[1].__name__):
                driver = None
                try:
                    driver = self.start_driver(browser)
                    self.assertIsInstance(driver(), browser[1])
                finally:
                    if driver:
                        driver.quit()

    def test_SeleniumLoadURL(self):
        url = "https://www.google.ca"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    selenium.load_url(driver, url)
                    self.assertEqual(driver().title, "Google")
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumLoadFile(self):
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    selenium.load_file(driver, self.test_page_url)
                    self.assertEqual(driver().title, "Page One")
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumLoadLocalPage(self):
        page = {
            "title": "Page One",
            "url": self.test_page_url,
            "alt-url": "alt/url",
            "page_id":
            {
                "method": "element",
                "identifier": "btnColor"
            },
            "elements":
            {
                "btnColor":
                {
                    "by": "id",
                    "value": "btnColor"
                },
                "nameField":
                {
                    "by": "id",
                    "value": "nameField"
                },
                "btnX":
                {
                    "by": "id",
                    "value": "btn-x"
                }
            }
        }
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    PageReader().add_page('test', page)
                    selenium.load_page(driver,
                                       ('custom', 'test'),
                                       use_local=True)
                    self.assertEqual(driver().title, "Page One")
            finally:
                if driver:
                    driver.quit()
                PageReader.reset()

    def test_SeleniumLoadPage(self):
        page = {
            "title": "Google",
            "url": "http://www.google.ca",
            "page_id":
            {
                "method": "title",
                "identifier": "Google"
            },
            "elements":
            {}
        }
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    PageReader().add_page('test', page)
                    selenium.load_page(driver, ('custom', 'test'))
                    self.assertEqual(driver().title, "Google")
            finally:
                if driver:
                    driver.quit()
                PageReader.reset()


class TestSeleniumLocateActions(TestSelenium):

    def test_SeleniumLocateFormated(self):
        locator = {"by": "xpath", "value": "//testing/{}/{}/{}"}
        args = ["locator", "formatting", "implementation"]
        expected = "//testing/locator/formatting/implementation"

        loc_out = selenium.locate(None, locator, args)

        self.assertEqual(loc_out['value'], expected)

    def test_SeleniumLocateFormattedPage(self):
        page = {
            "title": "Page One",
            "url": "tests/pages/page1.html",
            "alt-url": "alt/url",
            "page_id":
            {
                "method": "element",
                "identifier": "btnColor"
            },
            "elements":
            {
                "btnColor":
                {
                    "by": "id",
                    "value": "btn{}"
                }
            }
        }
        try:
            PageReader().add_page('test', page)

            args = ["Color"]
            locator = "btnColor"
            loc_out = selenium.locate(["custom", "test"], locator, args)
            self.assertEqual(loc_out['value'], 'btnColor')

            args = ["Red"]
            locator = PageReader().get_element(
                                    "custom",
                                    "test",
                                    "btnColor")
            loc_out = selenium.locate(["custom", "test"], locator, args)
            self.assertEqual(loc_out['value'], 'btnRed')
        finally:
            PageReader.reset()


class TestSeleniumBasicActions(TestSelenium):

    def test_SeleniumClose(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    driver().switch_to.new_window('tab')
                    before = len(driver().window_handles)
                    selenium.close(driver)
                    after = len(driver().window_handles)
                    self.assertEqual(before, 2)
                    self.assertEqual(after, 1)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumQuit(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    selenium.quit(driver)
                    self.assertIsNone(driver._driver)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumClick(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    selenium.click(driver,
                                   locator={"by": "id", "value": "btnColor"})
                    until = EC.presence_of_element_located
                    wait = driver.wait_until
                    locator = ("xpath", "//button[contains(@style, 'salmon')]")
                    self.assertIsNotNone(wait(
                                         until_func=until,
                                         locator=locator
                                         ))
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumWrite(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    text = 'Selenium Test Type'
                    selenium.write(
                        driver, text=text,
                        locator={"by": "id", "value": "nameField"})
                    self.assertEqual(
                        driver()
                        .find_element('id', 'nameField')
                        .get_attribute('value'), text)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumClear(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    text = 'Selenium Test Type'
                    driver().find_element('id', 'nameField').send_keys(text)
                    self.assertEqual(
                        driver()
                        .find_element('id', 'nameField')
                        .get_attribute('value'), text)
                    selenium.clear(
                        driver,
                        locator={"by": "id", "value": "nameField"})
                    self.assertEqual(
                        driver()
                        .find_element('id', 'nameField')
                        .get_attribute('value'), '')
            finally:
                if driver:
                    driver.quit()


class TestSeleniumReadOnlyActions(TestSelenium):

    def test_SeleniumReadAttribute(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    self.assertEqual(selenium.read_attribute(
                            driver, attribute='name',
                            locator={"by": "id", "value": "btn2"}), 'button2')
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumReadCSS(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    self.assertEqual(selenium.read_css(
                            driver, attribute='width',
                            locator={"by": "id", "value": "btn1"}), '300px')
            finally:
                if driver:
                    driver.quit()


class TestSeleniumWindowControlActions(TestSelenium):

    def test_SeleniumSwitchToFrameId(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):

                        driver().get(url)
                        selenium.switch_frame(driver, frame='FrameA')
                        btnName = driver().find_element(
                            *('id', 'btnColor')).get_attribute('name')
                        self.assertEqual(btnName, 'buttonAlpha')
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumSwitchToFrameElement(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    locator = {
                        'by': 'xpath',
                        'value': '//iframe[@title="Iframe 2"]'
                        }
                    selenium.switch_frame(driver, frame={
                                        'locator': locator
                                        })
                    btnName = driver().find_element(
                        *('id', 'btnColor')).get_attribute('name')
                    self.assertEqual(btnName, 'buttonAlpha')
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumSwitchWindowNoTitle(self):
        url_0 = pathlib.Path(self.test_page_url).resolve().as_uri()
        url_1 = 'https://www.google.ca'
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url_1)
                    driver().switch_to.new_window('tab')
                    driver().get(url_0)
                    self.assertEqual(driver().title, 'Page One')
                    selenium.switch_window(driver)
                    self.assertEqual(driver().title, 'Google')
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumSwitchWindowClosed(self):
        url_0 = pathlib.Path(self.test_page_url).resolve().as_uri()
        url_1 = 'https://www.google.ca'
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url_0)
                    driver().switch_to.new_window('tab')
                    driver().get(url_1)
                    self.assertEqual(driver().title, 'Google')
                    driver().close()
                    selenium.switch_window(driver)
                    self.assertEqual(driver().title, 'Page One')
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumSwitchWindowByTitle(self):
        url_0 = pathlib.Path(self.test_page_url).resolve().as_uri()
        url_1 = 'https://www.google.ca'
        url_2 = 'https://www.statcan.gc.ca/en/start'
        google = 'Google'
        pageOne = 'Page One'
        statcan = "Statistics Canada: Canada's national statistical agency"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url_1)
                    driver().switch_to.new_window('tab')
                    driver().get(url_2)
                    driver().switch_to.new_window('tab')
                    driver().get(url_0)
                    self.assertEqual(driver().title, pageOne)
                    selenium.switch_window(driver, google)
                    self.assertEqual(driver().title, google)
                    selenium.switch_window(driver, statcan)
                    self.assertEqual(driver().title, statcan)
                    selenium.switch_window(driver, pageOne)
                    self.assertEqual(driver().title, pageOne)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumSwitchWindowByPageTitle(self):
        google = {
            "title": "Google",
            "url": "http://www.google.ca",
            "page_id":
            {
                "method": "title",
            },
            "elements":
            {}
        }

        statcan = {
            "title": "Statistics Canada: Canada's national statistical agency",
            "url": "https://www.statcan.gc.ca/en/start",
            "page_id":
            {
                "method": "title",
            },
            "elements":
            {}
        }

        page_1 = {
            "title": "Page One",
            "url": pathlib.Path(self.test_page_url).resolve().as_uri(),
            "page_id":
            {
                "method": "title",
            },
            "elements":
            {}
        }
        PageReader().add_page('google', google)
        PageReader().add_page('statcan', statcan)
        PageReader().add_page('page1', page_1)

        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(google['url'])
                    driver().switch_to.new_window('tab')
                    driver().get(statcan['url'])
                    driver().switch_to.new_window('tab')
                    driver().get(page_1['url'])
                    self.assertEqual(driver().title, page_1['title'])
                    selenium.switch_window(driver, page=('custom', 'google'))
                    self.assertEqual(driver().title, google['title'])
                    selenium.switch_window(driver, page=('custom', 'statcan'))
                    self.assertEqual(driver().title, statcan['title'])
                    selenium.switch_window(driver, page=('custom', 'page1'))
                    self.assertEqual(driver().title, page_1['title'])

            finally:
                if driver:
                    driver.quit()
        PageReader.reset()


class TestSeleniumDropdownActions(TestSelenium):

    def test_SeleniumSelectDropdownByText(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    locator = {'by': 'id', 'value': 'dropdown'}
                    selenium.select_dropdown(driver, 'AA', 'text',
                                             locator=locator)
                    sel = Select(driver().find_element('id', 'dropdown'))
                    self.assertEqual(sel.first_selected_option.text, 'AA')
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumSelectDropdownByValue(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    locator = {'by': 'id', 'value': 'dropdown'}
                    selenium.select_dropdown(driver, 'last', 'value',
                                             locator=locator)
                    sel = Select(driver().find_element('id', 'dropdown'))
                    self.assertEqual(sel.first_selected_option.text, 'AA')
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumSelectDropdownByIndex(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    locator = {'by': 'id', 'value': 'dropdown'}
                    selenium.select_dropdown(driver, 3, 'index',
                                             locator=locator)
                    sel = Select(driver().find_element('id', 'dropdown'))
                    self.assertEqual(sel.first_selected_option.text, 'AA')
            finally:
                if driver:
                    driver.quit()


class TestSeleniumAssertActions(TestSelenium):

    def test_SeleniumAssertTextDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        text = "NEXT"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_contains_text(
                            driver,
                            text,
                            locator={"by": "id", "value": "nextBtn"})
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPartialTextDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        text = "EX"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_contains_text(
                            driver,
                            text,
                            locator={"by": "id", "value": "nextBtn"})
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertTextDisplayedSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        text = "FAIL"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_contains_text(
                            driver,
                            text, soft=True,
                            locator={"by": "id", "value": "nextBtn"})
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertTextDisplayedFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        text = "FAIL"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_contains_text(
                            driver,
                            text,
                            locator={"by": "id", "value": "nextBtn"})
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertExactTextDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        text = "NEXT"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_contains_text(
                            driver,
                            text,
                            locator={"by": "id", "value": "nextBtn"},
                            exact=True)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertExactTextDisplayedSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        text = "NEX"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_contains_text(
                            driver,
                            text, soft=True,
                            locator={"by": "id", "value": "nextBtn"},
                            exact=True)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertExactTextDisplayedFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        text = "NEX"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_contains_text(
                            driver,
                            text,
                            locator={"by": "id", "value": "nextBtn"},
                            exact=True)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_displayed(
                            driver,
                            locator={"by": "id", "value": "btn1"})
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertDisplayedFailed(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_displayed(
                            driver,
                            locator={"by": "id", "value": "btn-x"})

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertDisplayedSoftSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_displayed(
                            driver, soft=True,
                            locator={"by": "id", "value": "btn1"})
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertDisplayedSoftFailed(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_displayed(
                            driver, soft=True,
                            locator={"by": "id", "value": "btn-x"})

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertNotDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_not_displayed(
                            driver,
                            locator={"by": "id", "value": "btn-x"})
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertNotDisplayedFailed(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_not_displayed(
                            driver,
                            locator={"by": "id", "value": "btn1"})

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertNotDisplayedSoftSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_not_displayed(
                            driver, soft=True,
                            locator={"by": "id", "value": "btn-x"})
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertNotDisplayedSoftFailed(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_not_displayed(
                            driver, soft=True,
                            locator={"by": "id", "value": "btn1"})

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    page = {'identifier': 'Page One1',
                            'method': 'title'}
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_page_is_open(
                            driver, soft=True, page_id=page)

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByURLSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    page = {'identifier': 'not the url',
                            'method': 'url'}
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_page_is_open(
                            driver, soft=True, page_id=page)

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByElementSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    page = {
                        'identifier': {
                            'by': 'id',
                            'value': 'noElement'
                            },
                        'method': 'element'
                        }
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_page_is_open(
                            driver, page_id=page,
                            soft=True)

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleSoftSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    page = {'identifier': 'Page One',
                            'method': 'title'}
                    try:
                        selenium.assert_page_is_open(
                            driver, soft=True, page_id=page)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByURLSoftSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_page_is_open(
                            driver, soft=True, page_id={
                                                    'identifier': url,
                                                    'method': 'url'})
                    except TassAssertionError as e:
                        self.fail(e.message)

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByElementSoftSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
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
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_page_is_open(
                            driver, page_id={
                                        'identifier': 'Page One1',
                                        'method': 'title'})

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByURLFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    page = {'identifier': 'not the url',
                            'method': 'url'}
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_page_is_open(
                            driver, page_id=page)

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByElementFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_page_is_open(
                            driver, page_id={
                                        'identifier': {
                                            'by': 'id',
                                            'value': 'noElement'
                                            },
                                        'method': 'element'
                                        })

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByTitleSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_page_is_open(
                            driver, page_id={
                                        'identifier': 'Page One',
                                        'method': 'title'})
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByURLSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_page_is_open(
                            driver, page_id={
                                                    'identifier': url,
                                                    'method': 'url'})
                    except TassAssertionError as e:
                        self.fail(e.message)

            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPageIsOpenByElementSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
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
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertAttributeDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()

        value = "title-test"
        attribute = "test-id"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            locator={"by": "xpath", "value": "//title"})
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertPartialAttributeDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()

        value = "title"
        attribute = "test-id"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            locator={"by": "xpath", "value": "//title"})
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertAttributeDisplayedSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        value = "FAIL"
        attribute = "test-id"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            soft=True,
                            locator={"by": "xpath", "value": "//title"})
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertAttributeDisplayedFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        value = "FAIL"
        attribute = "test-id"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            locator={"by": "xpath", "value": "//title"})
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertExactAttributeDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        value = "title-test"
        attribute = "test-id"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        selenium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            locator={"by": "xpath", "value": "//title"},
                            exact=True)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertExactAttributeDisplayedSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        value = "FAIL"
        attribute = "test-id"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            soft=True,
                            locator={"by": "xpath", "value": "//title"},
                            exact=True)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertExactAttributeDisplayedFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        value = "FAIL"
        attribute = "test-id"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            locator={"by": "xpath", "value": "//title"},
                            exact=True)
            finally:
                if driver:
                    driver.quit()


class SeleniumScreenshotActions(TestSelenium):

    def test_SeleniumScreenshotPage(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        name = "test"
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        out = pathlib.Path(
                            selenium.screenshot(
                                driver,
                                name=name
                                )).resolve()
                        self.assertTrue(out.exists() and out.is_file())
                    finally:
                        if out.exists() and out.is_file():
                            out.unlink()
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumScreenshotElement(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        name = "test"
        locator = {"by": "id", "value": "btnColor"}
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    try:
                        out = pathlib.Path(
                            selenium.screenshot(
                                driver,
                                name=name,
                                locator=locator
                                )).resolve()
                        self.assertTrue(out.exists() and out.is_file())
                    finally:
                        if out.exists() and out.is_file():
                            out.unlink()
            finally:
                if driver:
                    driver.quit()


class TestSeleniumAlertActions(TestSelenium):

    def test_SeleniumHandleAlertAccept(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.alert('testing')"
                    driver().execute_script(alertScript)
                    selenium.handle_alert(driver)
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumHandleAlertAccept1(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.alert('testing')"
                    driver().execute_script(alertScript)
                    selenium.handle_alert(driver, handle=1)
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumHandleAlertAcceptStr(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.alert('testing')"
                    driver().execute_script(alertScript)
                    selenium.handle_alert(driver, handle='accept')
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumHandleAlertDismiss(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.alert('testing')"
                    driver().execute_script(alertScript)
                    selenium.handle_alert(driver, handle=False)
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumHandleAlertDismiss0(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.alert('testing')"
                    driver().execute_script(alertScript)
                    selenium.handle_alert(driver, handle=0)
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumHandleAlertDismissStr(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.alert('testing')"
                    driver().execute_script(alertScript)
                    selenium.handle_alert(driver, handle='dismiss')
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumHandleConfirmationAlertAccept(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.confirm('testing')"
                    driver().execute_script(alertScript)
                    selenium.handle_alert(driver)
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumHandleConfirmationAlertDismiss(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.confirm('testing')"
                    driver().execute_script(alertScript)
                    selenium.handle_alert(driver, handle='dismiss')
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumHandlePromptAlertAccept(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.promptResponse = prompt('testing')"
                    promptScript = "return window.promptResponse"
                    driver().execute_script(alertScript)
                    selenium.handle_alert(driver, text="abc")
                    self.assertIsNotNone(driver().title)
                    response = driver().execute_script(promptScript)
                    self.assertEqual(response, "abc")
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumHandlePromptAlertDismiss(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.promptResponse = prompt('testing')"
                    promptScript = "return window.promptResponse"
                    driver().execute_script(alertScript)
                    selenium.handle_alert(driver,
                                        handle='dismiss',
                                        text="abc")
                    self.assertIsNotNone(driver().title)
                    response = driver().execute_script(promptScript)
                    self.assertIsNone(response)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertAlertDisplayedSoftFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_alert_displayed(driver,soft=True)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertAlertDisplayedHardFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = self.start_driver(browser)
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_alert_displayed(driver, soft=False)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertAlertTextDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = new_driver(**browser[0])
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.alert('testing')"
                    driver().execute_script(alertScript)
                    selenium.assert_alert_displayed(driver, text="testing")
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertAlertPartialTextDisplayedSuccess(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = new_driver(**browser[0])
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.alert('testing')"
                    driver().execute_script(alertScript)
                    selenium.assert_alert_displayed(driver, text="test")
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertAlertTextDisplayedFailureSoft(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = new_driver(**browser[0])
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.alert('testing')"
                    driver().execute_script(alertScript)
                    with self.assertRaises(TassSoftAssertionError):
                        selenium.assert_alert_displayed(driver, text="FAIL", soft=True)
            finally:
                if driver:
                    driver.quit()

    def test_SeleniumAssertAlertTextDisplayedFailure(self):
        url = pathlib.Path(self.test_page_url).resolve().as_uri()
        for browser in self.drivers:
            driver = None
            try:
                driver = new_driver(**browser[0])
                with self.subTest(browser=browser[1].__name__):
                    driver().get(url)
                    alertScript = "window.alert('testing')"
                    driver().execute_script(alertScript)
                    with self.assertRaises(TassHardAssertionError):
                        selenium.assert_alert_displayed(driver, text="FAIL")
            finally:
                if driver:
                    driver.quit()
