import unittest
import importlib
import pathlib
from sys import platform
from tass.core.drivers.new_driver import new_driver
from tass.core.tools.page_reader import PageReader
from tass.core.exceptions.assertion_errors import (
    TassAssertionError,
    TassHardAssertionError,
    TassSoftAssertionError)
from tass.core.drivers.browser.customdrivers import ChromeDriver as CDriver
from selenium.webdriver.support.select import Select
import tass.core.actions.mobile.appium as appium
import selenium.webdriver.support.expected_conditions as EC




appium_inst = importlib.util.find_spec("appium")

pages = {
    # QA Practice

    "btn-page": {
            "title": "Buttons | Simple Button | QA Practice",
            "url": "https://www.qa-practice.com/elements/button/simple",
            "page_id":
            {
                "method": "title",
                "identifier": "Buttons | Simple Button | QA Practice"
            },
            "elements":
            {
                "btn":
                {
                    "by": "id",
                    "value": "submit-id-submit"
                },
                "click-confirm":
                {
                    "by": "id",
                    "value": "result-text"
                },
                "req-txt": {
                    "by": "id",
                    "value": "req_text"
                }
            }
        },
    "txt-page": {
        "title": "Input Field | Text Input | QA Practice",
        "url": "https://www.qa-practice.com/elements/input/simple",
        "page_id": {
            "method": "url",
            "identifier": "https://www.qa-practice.com/elements/input/simple"
        },
        "elements": {
            "input": {
                "by": "id",
                "value": "id_text_string"
            }
        }
    },
    "frm-page": {
        "title": "Iframes | Iframe | QA Practice",
        "url": "https://www.qa-practice.com/elements/iframe/iframe_page",
        "page_id": {
            "method": "title"
        },
        "elements": {
            "frame": {
                "by": "xpath",
                "value": "//*[@id='content']/iframe"
            },
            "main-btn": {
                "by": "xpath",
                "value": "//section/descendant::a[1]"
            }
        }
    },
    "drpdnw-page": {
        "title": "Select Input | Single Select | QA Practice",
        "url": "https://www.qa-practice.com/elements/select/single_select",
        "page_id": {
            "method": "element",
            "identifier": {
                "by": "id",
                "value": "id_choose_language"
            }
        },
        "elements": {
            "select": {
                "by": "id",
                "value": "id_choose_language"
            }
        }
    },
    "alrt-page": {
        "title": "Alerts | Alert Box | QA Practice",
        "url": "https://www.qa-practice.com/elements/alert/alert",
        "page_id": {
            "method": "title"
        },
        "elements": {
            "btn": {
                "by": "xpath",
                "value": "//*[@id='content']/a[1]"
            }
        }
    },
    "conf-page": {
        "title": "Alerts | Confirm Box | QA Practice",
        "url": "https://www.qa-practice.com/elements/alert/confirm",
        "page_id": {
            "method": "title"
        },
        "elements": {
            "btn": {
                "by": "xpath",
                "value": "//*[@id='content']/a[1]"
            },
            "result": {
                "by": "id",
                "value": "result-text"
            }
        }
    },
    "prmt-page": {
        "title": "Alerts | Prompt Box | QA Practice",
        "url": "https://www.qa-practice.com/elements/alert/prompt",
        "page_id": {
            "method": "title"
        },
        "elements": {
            "btn": {
                "by": "xpath",
                "value": "//*[@id='content']/a[1]"
            },
            "result": {
                "by": "id",
                "value": "result-text"
            }
        }
    }
}

@unittest.skipUnless(appium_inst, "Appium is not installed.")
class TestAppium(unittest.TestCase):

    config = [
        {
            "driver_name": "android",
            "uuid": "androidTEST",
            "configs": {
                "driver": {
                    "implicit_wait": "15",
                    "explicit_wait": "30"
                },
                "appium:server": {
                    "--allow-insecure": "uiautomator2:chromedriver_autodownload"
                },
                "appium:driver": {}
            }
        },
        {
            "driver_name": "ios",
            "uuid": "iosTEST",
            "configs": {
                "driver": {
                    "implicit_wait": "15",
                    "explicit_wait": "30"
                },
                "appium:server": {},
                "appium:driver": {}
            }
        }
    ]


    def setUpClass():
        from tass.core.drivers.mobile.appium_service import TASSAppiumService
        from tass.core.drivers.mobile.customdrivers import (
            AndroidDriver as Android,
            IOSDriver as IOS
            )

        TestAppium.drivers = [(TestAppium.config[0], Android)]
        if platform == "darwin":
            TestAppium.drivers.append((TestAppium.config[1], IOS))

    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")



    def appium_starter(self, devices):
        # Generator for Appium services and drivers.
        for device in devices:
            service = None
            print("\nStarting driver for: %s" % device[1].__name__)
            driver = new_driver(**device[0])
            try:
                service = TASSAppiumService.service(driver)
                TASSAppiumService.start_service(service)
            except Exception as e:
                print("\nERROR: Unable to start Appium service. Check Appium Server Installation.")
                raise e

            try:
                driver()
            except Exception as e:
                print("\nERROR: Unable to launch driver. Check driver installation and devices/emulators.")
                raise e

            yield device, driver
            TASSAppiumService.stop_service(service)


class TestAppiumStartupActions(TestAppium):
    def test_AppiumNewDriver(self):
        for device, driver in self.appium_starter(self.drivers):
            with self.subTest(device=device[1].__name__):
                try:
                    self.assertIsInstance(driver(), device[1])
                finally:
                    if driver:
                        driver.quit()

    def test_AppiumLoadURL(self):
        url = "https://www.google.ca"
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    appium.load_url(driver, url)
                    self.assertEqual(driver().title, "Google")
            finally:
                if driver:
                    driver.quit()


class TestAppiumBasicActions(TestAppium):
    def test_AppiumClose(self):
        url = "https://www.google.ca"
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    driver().get(url)
                    driver().switch_to.new_window('tab')
                    before = len(driver().window_handles)
                    appium.close(driver)
                    after = len(driver().window_handles)
                    self.assertGreater(before, after)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumQuit(self):
        url = "https://www.google.ca"
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    driver().get(url)
                    appium.quit(driver)
                    self.assertIsNone(driver._driver)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumClick(self):
        url = pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    driver().get(url)
                    appium.click(driver,
                                   locator=pages['btn-page']['elements']['btn'])
                    until = EC.presence_of_element_located
                    wait = driver.wait_until
                    _ = pages["btn-page"]['elements']['click-confirm']
                    locator = (_['by'], _['value'])
                    self.assertIsNotNone(wait(
                                         until_func=until,
                                         locator=locator
                                         ))
            finally:
                if driver:
                    driver.quit()

    def test_AppiumWrite(self):
        url = pages['txt-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    driver().get(url)
                    text = 'Selenium Test Type'
                    appium.write(
                        driver, text=text,
                        locator=pages['txt-page']['elements']['input'])
                    self.assertEqual(
                        driver()
                        .find_element(**pages['txt-page']['elements']['input'])
                        .get_attribute('value'), text)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumClear(self):
        url = pages['txt-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    driver().get(url)
                    text = 'Selenium Test Type'
                    locator = pages['txt-page']['elements']['input']
                    driver().find_element(**locator).send_keys(text)
                    self.assertEqual(
                        driver()
                        .find_element(**locator)
                        .get_attribute('value'), text)
                    appium.clear(
                        driver,
                        locator=locator)
                    self.assertEqual(
                        driver()
                        .find_element(**locator)
                        .get_attribute('value'), '')
            finally:
                if driver:
                    driver.quit()


class TestAppiumReadOnlyActions(TestAppium):

    def test_AppiumReadAttribute(self):
        url = pages['btn-page']['url']
        expected = "btn btn-primary"
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    driver().get(url)
                    self.assertEqual(appium.read_attribute(
                            driver, attribute='class',
                            locator=pages['btn-page']['elements']['btn']),
                            expected)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumReadCSS(self):
        url = pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    driver().get(url)
                    self.assertEqual(appium.read_css(
                            driver, attribute='display',
                            locator=pages['btn-page']['elements']['btn']), 'inline-block')
            finally:
                if driver:
                    driver.quit()


class TestAppiumWindowControlActions(TestAppium):

    def test_AppiumSwitchToFrameId(self):
        # TODO: Not testable on qa-practice
        self.skipTest("Not currently testable")

    def test_AppiumSwitchToFrameElement(self):
        url = pages['frm-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    driver().get(url)
                    locator = pages['frm-page']['elements']['frame']
                    appium.switch_frame(driver, frame={
                                        'locator': locator
                                        })
                    btn = driver().find_element(
                        **pages['frm-page']['elements']['main-btn']).get_attribute('class')
                    self.assertEqual(btn, 'btn btn-primary my-2')
            finally:
                if driver:
                    driver.quit()

    def test_AppiumSwitchWindowNoTitle(self):
        url_0 = pages["btn-page"]['url']
        url_1 = 'https://www.google.ca'
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    driver().get(url_1)
                    driver().switch_to.new_window('tab')
                    driver().get(url_0)
                    self.assertEqual(driver().title, pages['btn-page']['title'])
                    appium.switch_window(driver)
                    self.assertEqual(driver().title, 'Google')
            finally:
                if driver:
                    driver.quit()

    def test_AppiumSwitchWindowClosed(self):
        url_0 = pages['btn-page']['url']
        url_1 = 'https://www.google.ca'
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(device=device[1].__name__):
                    driver().get(url_0)
                    driver().switch_to.new_window('tab')
                    driver().get(url_1)
                    self.assertEqual(driver().title, 'Google')
                    driver().close()
                    appium.switch_window(driver)
                    self.assertEqual(driver().title, pages['btn-page']['title'])
            finally:
                if driver:
                    driver.quit()

    def test_AppiumSwitchWindowByTitle(self):
        url_0 = pages['btn-page']['url']
        url_1 = 'https://www.google.ca'
        url_2 = 'https://www.statcan.gc.ca/en/start'
        google = 'Google'
        pageOne = pages['btn-page']['title']
        statcan = "Statistics Canada: Canada's national statistical agency"
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url_1)
                    driver().switch_to.new_window('tab')
                    driver().get(url_2)
                    driver().switch_to.new_window('tab')
                    driver().get(url_0)
                    self.assertEqual(driver().title, pageOne)
                    appium.switch_window(driver, title=google)
                    self.assertEqual(driver().title, google)
                    appium.switch_window(driver, title=statcan)
                    self.assertEqual(driver().title, statcan)
                    appium.switch_window(driver, title=pageOne)
                    self.assertEqual(driver().title, pageOne)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumSwitchWindowByPageTitle(self):
        PageReader().add_page('btn-page', pages["btn-page"])
        PageReader().add_page('txt-page', pages["txt-page"])
        PageReader().add_page('frm-page', pages["frm-page"])

        btn = pages["btn-page"]
        txt = pages["txt-page"]
        frm = pages["frm-page"]

        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(btn['url'])
                    driver().switch_to.new_window('tab')
                    driver().get(txt['url'])
                    driver().switch_to.new_window('tab')
                    driver().get(frm['url'])
                    self.assertEqual(driver().title, frm['title'])
                    appium.switch_window(driver, page=('custom', 'btn-page'))
                    self.assertEqual(driver().title, btn['title'])
                    appium.switch_window(driver, page=('custom', 'txt-page'))
                    self.assertEqual(driver().title, txt['title'])
                    appium.switch_window(driver, page=('custom', 'frm-page'))
                    self.assertEqual(driver().title, frm['title'])

            finally:
                if driver:
                    driver.quit()


class TestAppiumDropdownActions(TestAppium):

    def test_AppiumSelectDropdownByText(self):
        url = pages['drpdnw-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    locator = pages['drpdnw-page']['elements']['select']
                    appium.select_dropdown(driver, 'Python', 'text',
                                             locator=locator)
                    sel = Select(driver().find_element(**locator))
                    self.assertEqual(sel.first_selected_option.text, 'Python')
            finally:
                if driver:
                    driver.quit()

    def test_AppiumSelectDropdownByValue(self):
        url = pages['drpdnw-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    locator = pages['drpdnw-page']['elements']['select']
                    appium.select_dropdown(driver, '1', 'value',
                                             locator=locator)
                    sel = Select(driver().find_element(**locator))
                    self.assertEqual(sel.first_selected_option.text, 'Python')
            finally:
                if driver:
                    driver.quit()

    def test_AppiumSelectDropdownByIndex(self):
        url = pages['drpdnw-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    locator = pages['drpdnw-page']['elements']['select']
                    appium.select_dropdown(driver, 1, 'index',
                                             locator=locator)
                    sel = Select(driver().find_element(**locator))
                    self.assertEqual(sel.first_selected_option.text, 'Python')
            finally:
                if driver:
                    driver.quit()


class TestAppiumAssertActions(TestAppium):

    def test_AppiumAssertTextDisplayedSuccess(self):
        url = pages['btn-page']['url']
        text = "Submitted"
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    try:
                        appium.assert_contains_text(
                            driver,
                            text,
                            locator=txt)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPartialTextDisplayedSuccess(self):
        url = pages['btn-page']['url']
        text = "ubmit"
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    try:
                        appium.assert_contains_text(
                            driver,
                            text,
                            locator=txt)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertTextDisplayedSoftFailure(self):
        url = pages['btn-page']['url']
        text = "FAIL"
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_contains_text(
                            driver,
                            text,
                            soft=True,
                            locator=txt)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertTextDisplayedFailure(self):
        url = pages['btn-page']['url']
        text = "FAIL"
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_contains_text(
                            driver,
                            text,
                            locator=txt)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertExactTextDisplayedSuccess(self):
        url = pages['btn-page']['url']
        text = "Submitted"
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    try:
                        appium.assert_contains_text(
                            driver,
                            text,
                            locator=txt,
                            exact=True)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertExactTextDisplayedSoftFailure(self):
        url = pages['btn-page']['url']
        text = "FAIL"
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_contains_text(
                            driver,
                            text,
                            soft=True,
                            locator=txt,
                            exact=True)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertExactTextDisplayedFailure(self):
        url = pages['btn-page']['url']
        text = "FAIL"
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_contains_text(
                            driver,
                            text,
                            locator=txt,
                            exact=True)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertDisplayedSuccess(self):
        url = pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    try:
                        appium.assert_displayed(
                            driver,
                            locator=txt)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertDisplayedFailed(self):
        url = pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                hidden = pages['btn-page']['elements']['req-txt']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_displayed(
                            driver,
                            locator=hidden)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertDisplayedSoftSuccess(self):
        url = pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    try:
                        appium.assert_displayed(
                            driver,
                            locator=txt,
                            soft=True)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertDisplayedSoftFailed(self):
        url = pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                hidden = pages['btn-page']['elements']['req-txt']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_displayed(
                            driver,
                            soft=True,
                            locator=hidden)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertNotDisplayedSuccess(self):
        url = pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                hidden = pages['btn-page']['elements']['req-txt']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    try:
                        appium.assert_not_displayed(
                            driver,
                            locator=hidden)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertNotDisplayedFailed(self):
        url = pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_not_displayed(
                            driver,
                            locator=txt)

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertNotDisplayedSoftSuccess(self):
        url = pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                hidden = pages['btn-page']['elements']['req-txt']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    try:
                        appium.assert_not_displayed(
                            driver,
                            locator=hidden,
                            soft=True)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertNotDisplayedSoftFailed(self):
        url = pages['btn-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                btn = pages['btn-page']['elements']['btn']
                txt = pages['btn-page']['elements']['click-confirm']
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**btn).click()
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_not_displayed(
                            driver,
                            locator=txt,
                            soft=True)

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByTitleSoftFailure(self):
        page = pages['btn-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get("https://www.google.ca")
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_page_is_open(
                            driver, soft=True, page_id=page['page_id'])

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByURLSoftFailure(self):
        page = pages['txt-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get("https://www.google.ca")
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_page_is_open(
                            driver, soft=True, page_id=page['page_id'])

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByElementSoftFailure(self):
        page = pages['drpdnw-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get("https://www.google.ca")
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_page_is_open(
                            driver, soft=True, page_id=page['page_id'])

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByTitleSoftSuccess(self):
        page = pages['btn-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(page['url'])
                    try:
                        appium.assert_page_is_open(
                            driver, soft=True, page_id=page['page_id'])
                    except TassAssertionError as e:
                        self.fail(e.message)

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByURLSoftSuccess(self):
        page = pages['txt-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(page['url'])
                    try:
                        appium.assert_page_is_open(
                            driver, soft=True, page_id=page['page_id'])
                    except TassAssertionError as e:
                        self.fail(e.message)

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByElementSoftSuccess(self):
        page = pages['drpdnw-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(page['url'])
                    try:
                        appium.assert_page_is_open(
                            driver, soft=True, page_id=page['page_id'])
                    except TassAssertionError as e:
                        self.fail(e.message)

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByTitleFailure(self):
        page = pages['btn-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get("https://www.google.ca")
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_page_is_open(
                            driver, page_id=page['page_id'])

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByURLFailure(self):
        page = pages['txt-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get("https://www.google.ca")
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_page_is_open(
                            driver, page_id=page['page_id'])

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByElementFailure(self):
        page = pages['drpdnw-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get("https://www.google.ca")
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_page_is_open(
                            driver, page_id=page['page_id'])

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByTitleSuccess(self):
        page = pages['btn-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(page['url'])
                    try:
                        appium.assert_page_is_open(
                            driver, page_id=page['page_id'])
                    except TassAssertionError as e:
                        self.fail(e.message)

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByURLSuccess(self):
        page = pages['txt-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(page['url'])
                    try:
                        appium.assert_page_is_open(
                            driver, page_id=page['page_id'])
                    except TassAssertionError as e:
                        self.fail(e.message)

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPageIsOpenByElementSuccess(self):
        page = pages['drpdnw-page']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(page['url'])
                    try:
                        appium.assert_page_is_open(
                            driver, page_id=page['page_id'])
                    except TassAssertionError as e:
                        self.fail(e.message)

            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertAttributeDisplayedSuccess(self):
        url = pages['btn-page']['url']
        element = pages['btn-page']['elements']['btn']

        value = "submit"
        attribute = "name"
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    try:
                        appium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            locator=element)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertPartialAttributeDisplayedSuccess(self):
        url = pages['btn-page']['url']
        element = pages['btn-page']['elements']['btn']

        value = "ubmi"
        attribute = "name"
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    try:
                        appium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            locator=element)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertAttributeDisplayedSoftFailure(self):
        url = pages['btn-page']['url']
        element = pages['btn-page']['elements']['btn']

        value = "FAIL"
        attribute = "name"
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            soft=True,
                            locator=element)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertAttributeDisplayedFailure(self):
        url = pages['btn-page']['url']
        element = pages['btn-page']['elements']['btn']

        value = "FAIL"
        attribute = "name"
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            locator=element)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertExactAttributeDisplayedSuccess(self):
        url = pages['btn-page']['url']
        element = pages['btn-page']['elements']['btn']

        value = "submit"
        attribute = "name"
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    try:
                        appium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            exact=True,
                            locator=element)
                    except TassAssertionError as e:
                        self.fail(e.message)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertExactAttributeDisplayedSoftFailure(self):
        url = pages['btn-page']['url']
        element = pages['btn-page']['elements']['btn']

        value = "submi"
        attribute = "name"
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            exact=True,
                            soft=True,
                            locator=element)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertExactAttributeDisplayedFailure(self):
        url = pages['btn-page']['url']
        element = pages['btn-page']['elements']['btn']

        value = "submi"
        attribute = "name"
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_attribute_contains_value(
                            driver,
                            attribute,
                            value,
                            exact=True,
                            locator=element)
            finally:
                if driver:
                    driver.quit()


class AppiumScreenshotActions(TestAppium):

    def test_AppiumScreenshotPage(self):
        url = pages['btn-page']['url']
        name = "test"
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    try:
                        out = pathlib.Path(
                            appium.screenshot(
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

    def test_AppiumScreenshotElement(self):
        url = pages['btn-page']['url']
        locator = pages['btn-page']['elements']['btn']
        name = "test"
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    try:
                        out = pathlib.Path(
                            appium.screenshot(
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


class TestAppiumAlertActions(TestAppium):

    def test_AppiumHandleAlertAccept(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['alrt-page']['elements']['btn']).click()
                    appium.handle_alert(driver)
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumHandleAlertAccept1(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['alrt-page']['elements']['btn']).click()
                    appium.handle_alert(driver, handle=1)
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumHandleAlertAcceptStr(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['alrt-page']['elements']['btn']).click()
                    appium.handle_alert(driver, handle='accept')
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumHandleAlertDismiss(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['alrt-page']['elements']['btn']).click()
                    appium.handle_alert(driver, handle=False)
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumHandleAlertDismiss0(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['alrt-page']['elements']['btn']).click()
                    appium.handle_alert(driver, handle=0)
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumHandleAlertDismissStr(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['alrt-page']['elements']['btn']).click()
                    appium.handle_alert(driver, handle='dismiss')
                    self.assertIsNotNone(driver().title)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumHandleConfirmationAlertAccept(self):
        url = pages['conf-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['conf-page']['elements']['btn']).click()
                    appium.handle_alert(driver)
                    result = driver().find_element(**pages['conf-page']['elements']['result']).text
                    self.assertEqual(result.lower(), "ok")
            finally:
                if driver:
                    driver.quit()

    def test_AppiumHandleConfirmationAlertDismiss(self):
        url = pages['conf-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['conf-page']['elements']['btn']).click()
                    appium.handle_alert(driver, handle='dismiss')
                    result = driver().find_element(**pages['conf-page']['elements']['result']).text
                    self.assertEqual(result.lower(), "cancel")
            finally:
                if driver:
                    driver.quit()

    def test_AppiumHandlePromptAlertAccept(self):
        url = pages['prmt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['prmt-page']['elements']['btn']).click()
                    appium.handle_alert(driver, text="abc")
                    self.assertIsNotNone(driver().title)
                    result = driver().find_element(**pages['prmt-page']['elements']['result']).text
                    self.assertEqual(result, "abc")
            finally:
                if driver:
                    driver.quit()

    def test_AppiumHandlePromptAlertDismiss(self):
        url = pages['prmt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['prmt-page']['elements']['btn']).click()
                    appium.handle_alert(driver, text="abc", handle='dismiss')
                    self.assertIsNotNone(driver().title)
                    result = driver().find_element(**pages['prmt-page']['elements']['result']).text
                    self.assertIn("canceled", result.lower())
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertAlertDisplayedSoftFailure(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_alert_displayed(driver, soft=True)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertAlertDisplayedHardFailure(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_alert_displayed(driver)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertAlertTextDisplayedSuccess(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):

            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['alrt-page']['elements']['btn']).click()
                    text = "I am an alert!"
                    appium.assert_alert_displayed(driver, text=text)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertAlertPartialTextDisplayedSuccess(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['alrt-page']['elements']['btn']).click()
                    text = "alert!"
                    appium.assert_alert_displayed(driver, text=text)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertAlertTextDisplayedFailureSoft(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['alrt-page']['elements']['btn']).click()
                    with self.assertRaises(TassSoftAssertionError):
                        appium.assert_alert_displayed(driver, text="FAIL", soft=True)
            finally:
                if driver:
                    driver.quit()

    def test_AppiumAssertAlertTextDisplayedFailure(self):
        url = pages['alrt-page']['url']
        for device, driver in self.appium_starter(self.drivers):
            try:
                with self.subTest(browser=device[1].__name__):
                    driver().get(url)
                    driver().find_element(**pages['alrt-page']['elements']['btn']).click()
                    with self.assertRaises(TassHardAssertionError):
                        appium.assert_alert_displayed(driver, text="FAIL")
            finally:
                if driver:
                    driver.quit()