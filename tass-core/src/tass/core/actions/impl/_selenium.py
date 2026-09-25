import pathlib
from datetime import datetime
from selenium.common.exceptions import (WebDriverException,
                                        NoSuchWindowException,
                                        NoAlertPresentException,
                                        NoSuchElementException)
from ...tools.page_reader import PageReader
from ...exceptions.assertion_errors import TassHardAssertionError
from ...exceptions.assertion_errors import TassSoftAssertionError
from ...log.logging import getLogger

#  For additional documentation, see selenium docs:
#  https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html


logger = getLogger(__name__)


def __is_displayed(driver, find, **kwargs):
    display = find(driver, **kwargs).is_displayed()
    logger.debug("Found element, displayed=%s", display)
    return display


def __switch_to_alert(driver):
    try:
        return driver.alert
    except NoAlertPresentException as e:
        logger.warning("No alert present to switch to.")
        raise e

def _click(driver, find, **kwargs):
    find(driver, **kwargs).click()
    logger.debug("Element clicked.")


def _write(driver, find, text='', **kwargs):
    find(driver, **kwargs).send_keys(text)
    logger.debug("Typed: '%s'", text)




def _write_stored_value(driver, find, text_key='', **kwargs):
    from .. import core
    text = core.read_value(text_key)
    _write(driver, find=find, text=text, **kwargs)


def _select_dropdown(driver, find, value, using, **kwargs):
    driver.select(find(driver, **kwargs), value, using)
    logger.debug("Dropdown selected: '%s' -- using: '%s'", value, using)


def _clear(driver, find, **kwargs):
    find(driver, **kwargs).clear()
    logger.debug("Element cleared.")


def _load_url(driver, url):
    driver().get(url)
    logger.debug("Loaded url in browser: %s", url)


def _load_file(driver, relative_path):
    url = pathlib.Path(relative_path).resolve().as_uri()
    logger.debug("Looking for file to open at: %s", url)
    driver().get(url)
    logger.debug("Loaded local file in browser.")


def _load_page(driver, page, url_key='url', use_local=False):
    url = PageReader().get_url(*page, url_key)
    logger.debug("Read url from POM: %s", url)
    if (use_local):
        _load_file(driver, url)
    else:
        _load_url(driver, url)


def _read_attribute(driver, find, attribute, **kwargs):
    attribute = str(attribute)
    attr = find(driver, **kwargs).get_attribute(attribute)
    logger.debug("Element has attribute: '%s'='%s'", attribute, attr)

    return attr


def _read_css(driver, find, attribute, **kwargs):
    attribute = str(attribute)
    prop = find(driver, **kwargs).value_of_css_property(attribute)
    logger.debug("Element has CSS property: '%s'='%s'", attribute, prop)

    return prop


def _read_text(driver, find, **kwargs):
    text = find(driver, **kwargs).text
    logger.info("Element has text: '%s'", text)

    return text


def _switch_frame(driver, find, frame, page):
    if page:
        _frame = PageReader().get_element(*page, frame)
        logger.debug("Found frame in POM.")
        _switch_frame(driver, _frame, page=None, find=find)
    elif (isinstance(frame, str)):
        driver().switch_to.frame(frame)
        logger.debug("Switched active frame to: %s", frame)
    else:
        element = find(driver, page=page, **frame)
        driver().switch_to.frame(element)
        logger.debug("Switched active frame to element: %r", element)


def _switch_window(driver, title=None, page=None):
    # TODO: Keep track of window handles to avoid loop?
    # TODO: Handle switching from closed tabs
    handles = driver().window_handles
    if len(handles) == 1:
        logger.info("Only one window/tab open. Switching to that window.")
        driver.switch_window(handles[0])
        return
    if len(handles) < 1:
        logger.warning("No windows open. Cannot switch.")
        return
    if (page):
        _switch_window(driver,
                      title=PageReader().get_page_title(*page),
                      page=None)
        return
    cur_handle = None
    try:
        cur_handle = driver().current_window_handle
        logger.debug("Current window handle: %s -- title: %s",
                     cur_handle, driver().title)
    except NoSuchWindowException:
        logger.info(
            "Current window closed or missing. Switching to other tab/window"
            )
    if (title is None):
        logger.info("Switching to next tab or window...")
        for handle in handles:
            # TODO: Handle switching if only 1 tab/window
            if (handle != cur_handle):
                driver.switch_window(handle)
                return
    elif (isinstance(title, str)):
        for handle in handles:
            if (handle == cur_handle):
                continue
            else:
                driver.switch_window(handle)
                if (driver().title == title):
                    return

    raise ValueError('No other window/tab with title: {}'.format(title))


def _close(driver):
    driver().close()
    logger.info("Closed currently active tab/window.")


def _quit(driver):
    driver.quit()
    logger.info("Driver exited browser session.")


def _handle_alert(driver, handle=True, text=None):
    alert_accept = None
    if handle and isinstance(handle, str):
        if handle.lower() == 'accept':
            alert_accept = True
        elif handle.lower() == 'dismiss':
            alert_accept = False
        else:
            logger.warning(f"Invalid handle function: {handle}")
            logger.warning("Will use default function.")
            alert_accept = True
    else:
        alert_accept = bool(handle)
    if alert_accept:
        driver.accept_alert(text=text)
    else:
        driver.dismiss_alert(text=text)


def _screenshot(driver,
               find,
               name="screenshot",
               locator=None,
               **kwargs):
    screenshotsfldr = pathlib.Path("screenshots").resolve()
    # Sort png by browser config
    driverfldr = [driver.os, driver.browser, driver.browser_version]
    screenshotsfldr = screenshotsfldr.joinpath(*driverfldr).resolve()
    screenshotsfldr.mkdir(exist_ok=True, parents=True)
    date_tag = datetime.now().strftime("%d-%m-%y--%H-%M-%S")
    name = name.replace(" ", "_")  # Remove spaces from file name
    file_name = "_".join([name, date_tag])
    _file = screenshotsfldr.joinpath(file_name).with_suffix(".png")
    count = 0

    while _file.exists():
        count += 1
        file_name = "".join([name, date_tag, f"({count})"])
        _file = _file.with_stem(file_name)

    out = str(_file.resolve())
    logger.info("Saving screenshot as: %s", out)

    if locator:
        status = find(driver, locator, **kwargs).screenshot(out)
    else:
        status = driver().save_screenshot(out)

    if status:
        logger.info("Screenshot saved successfully.")
    else:
        logger.warning("Screenshot was not saved!")

    return out


# / / / / / / / Assertions / / / / / / /
def __fail(soft, message, reason=None, exception=None, *args):
    if (soft):
        raise TassSoftAssertionError(
                message, reason=reason, *args) from exception
    else:
        raise TassHardAssertionError(
                message, reason=reason, *args)  from exception


def _assert_alert_displayed(driver, text=None, soft=False):
    def _check_alert(driver):
        try: 
            _ = __switch_to_alert(driver)
            logger.debug("Alert with text: '%s' is displayed.", _.text)
            return _
        except NoAlertPresentException as e:
            logger.warning("No alert present: %s", e)
            __fail(soft, "assert_alert_displayed", reason="No alert present")
    alert = _check_alert(driver)
    logger.debug("Alert found.")
    if text and isinstance(text, str):
        text_ok = text in alert.text
        if not text_ok:
            __fail(soft,
                "assert_alert_displayed",
                reason = f"Alert text does not contain expected text: {text}")
        else:
            logger.debug("Alert text contains expected text: %s", text)



def _assert_page_is_open(driver, find, page=None,
                        soft=False, page_id=None):
    def _element(driver, find, element, page, soft):
        ele = None
        try:
            ele = find(driver, locator=element, page=page)
            logger.debug("Element: %s found, page is open.", element)
        except NoSuchElementException as e:
            logger.warning('Exception raised: %s', e)
            __fail(soft,
            "assert_page_is_open",
            exception=e)

        logger.info("Element found. Page is open")

        if (ele is None):
            __fail(soft,
                "assert_page_is_open",
                reason='Element {identifier} not found.')

    def _title(driver, find, title, soft, normalize=False):
        actual = driver().title
        if (actual != title):
            ele = None
            if normalize:
                ele_title = {
                    "by": "xpath",
                    "value": f"//title[normalize-space(text())='{title}']"
                    }
            else:
                ele_title = {
                    "by": "xpath",
                    "value": f"//title[text()='{title}']"
                    }
            try:
                ele = find(driver, locator=ele_title, page=page)
                actual = ele.text
                logger.debug("Element: %s found, page is open.", ele_title)
            except NoSuchElementException as e:
                logger.warning('Exception raised: %s', e)
                __fail(soft,
                    "assert_page_is_open",
                    exception=e)
            if not ele:
                __fail(soft,
                    "assert_page_is_open",
                    reason=f'Expected title not found. Actual page title: {actual}')

        logger.info("Found expected title. Page is open")

    def _url(driver, url, soft):
        actual = driver().current_url
        logger.info('Current url: %s', actual)
        if (actual != url):
            __fail(soft,
                "assert_page_is_open",
                reason=f'Expected url not open. Actual url: {actual}')

        logger.info("Found expected url. Page is open.")
    if (page is not None):
        page_id = PageReader().get_page_id(*page)

        match page_id.get('method', 'element'):
            case 'element':
                _element(driver,
                         find,
                         page_id['identifier'],
                         page,
                         soft)
            case 'normalize-title':
                title = page_id['identifier']
                _title(driver, find, title, soft, normalize=True)
            case 'title':
                title = page_id.get('identifier',
                                    PageReader().get_page_title(*page))
                _title(driver, find, title, soft)
            case 'url':
                url = page_id.get('identifier', PageReader().get_url(*page))
                _url(driver, url, soft)
            case _:
                raise ValueError(
                    f"Method, {page_id.get('method')} not supported")
    elif (page_id is not None):
        match page_id.get('method', 'element'):
            case 'element':
                _element(driver,
                         find,
                         page_id['identifier'],
                         None,
                         soft)
            case 'normalize-title':
                title = page_id['identifier']
                _title(driver, find, title, soft, normalize=True)
            case 'title':
                title = page_id['identifier']
                _title(driver, find, title, soft)
            case 'url':
                url = page_id['identifier']
                _url(driver, url, soft)
            case _:
                raise ValueError(
                    f"Method, {page_id.get('method')} not supported")
    elif (page is None and page_id is None):
        raise ValueError('Either page or page_id must not be None')


def _assert_contains_text(driver, find, text,
                         soft=False, exact=False, **kwargs):
    actual_text = None
    try:
        actual_text = _read_text(driver=driver, find=find, **kwargs)
        logger.info("Element contains text: %s", actual_text)
        if exact and text != actual_text:
            __fail(soft, "assert_text_contains -- exact match",
            reason=f"Actual text: {actual_text}")
        elif text not in actual_text:
            __fail(soft, "assert_text_contains -- partial match",
            reason=f"Actual text: {actual_text}")
        else:
            logger.info("Element contains text: %s", text)
    except NoSuchElementException as e:
        logger.debug("Driver reporting error. %r", kwargs)
        __fail(soft, "assert_text_contains",
            exception=e)


def _assert_displayed(driver, find, soft=False, **kwargs):
    """Assert the given element is displayed. Can be a soft or hard check

    Execute the selenium is_displayed function against the locator
    provided. Then return true if it is displayed.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element fuinction.
        soft:
            Boolean flag that indicates if a failed assertion
            should end execution. If True execution for the
            current test stops upon returning. If false, error is
            recorded and execution can continue. The default is False.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """
    try:
        if (__is_displayed(driver, find=find, **kwargs)):
            logger.info("Element is displayed.")
            return
        else:
            __fail(soft,
                "assert_displayed",
                reason="Element is not displayed.")
    except NoSuchElementException as e:
        logger.debug("Driver reporting error. %r", kwargs)
        __fail(soft,
            "assert_displayed",
            exception=e)


def _assert_not_displayed(driver, find, soft=False, **kwargs):
    try:
        if not (__is_displayed(driver, find=find, **kwargs)):
            logger.info("Element is not displayed.")
            return
        else:
            __fail(soft,
                "assert_not_displayed",
                reason="Element is displayed.")
    except NoSuchElementException as e:
        logger.debug("Driver reporting error. %r", kwargs)
        __fail(soft,
            "assert_not_displayed",
            exception=e)


def _assert_attribute_contains_value(driver, find, attribute, value,
                                     soft=False,
                                    exact=False, **kwargs):
    actual_value = _read_attribute(driver, attribute=attribute, find=find, **kwargs)
    logger.info("Element contains attribute: %s", actual_value)
    value = str(value)
    try:
        if exact and value != actual_value:
            __fail(soft,
                "assert_attribute_contains--exact match",
                reason=f"attribute: {attribute} is not exact match: {actual_value}")
        elif value not in actual_value:
            __fail(soft,
                "assert_attribute_contains--partial match", 
                reason=f"attribute: {attribute} does not contain match: {actual_value}")

        else:
            logger.info("Element contains attribute: %s with value: %s",
                        attribute, value)
    except NoSuchElementException as e:
        logger.debug("Driver reporting error. %r", kwargs)
        __fail(soft,
            "assert_attribute_contains_value",
            exception=e)
