import pathlib
from datetime import datetime
from selenium.common.exceptions import (WebDriverException,
                                        NoSuchWindowException,
                                        NoAlertPresentException)
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.alert import Alert
from ..tools.page_reader import PageReader
from ..exceptions.assertion_errors import TassHardAssertionError
from ..exceptions.assertion_errors import TassSoftAssertionError
from ..log.logging import getLogger

#  For additional documentation, see selenium docs:
#  https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html


logger = getLogger(__name__)


def locate(page, locator, locator_args):
    logger.debug("Locator: %s -- Args: %s", locator, locator_args)
    if (isinstance(locator, str)):
        logger.debug("Getting locator (%s) from POM: %s", locator, page)
        _loc = PageReader().get_element(*page, locator)
    elif isinstance(locator, dict):
        logger.debug("Locator provided directly...")
        _loc = locator
    else:
        msg = "Locator type not supported. Type: {}".format(type(locator))
        logger.error(msg)
        raise TypeError(msg)

    if locator_args:
        logger.debug("Filling in blanks in locator using: %s", locator_args)
        # scenario converter shold convert locator args to a list by default
        _loc['value'] = _loc['value'].format(*locator_args)

    logger.debug("Using locator: %s", _loc)
    return _loc


def _find_element(driver, locator, locator_args=None, page=None):
    logger.debug("Searching for element...")
    return driver().find_element(**locate(page, locator, locator_args))


def _is_displayed(driver, find=_find_element, **kwargs):
    try:
        display = find(driver, **kwargs).is_displayed()
        logger.debug("Found element, displayed=%s", display)
        return display
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        display = find(driver, **kwargs).is_displayed()
        logger.debug("Attempt 2 >> Found element, displayed=%s", display)
        return display


def click(driver, find=_find_element, **kwargs):
    """Click an element in the DOM

    Execute the selenium click function against the locator
    that is part of the kwargs argument. If a WebDriverException
    occurs the action is attempted a second time before
    allowing the exception to be raised to the next level.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element fuinction.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """
    try:
        find(driver, **kwargs).click()
        logger.debug("Element clicked.")
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        find(driver, **kwargs).click()
        logger.debug("Attempt 2 >> Element clicked.")


def write(driver, find=_find_element, text='', **kwargs):
    """Send a string to an element in the DOM

    Execute the selenium send_keys(str) function against the locator
    that is part of the kwargs argument. If a WebDriverException
    occurs the action is attempted a second time before
    allowing the exception to be raised to the next level.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element fuinction.
        text:
            The str text that is to be sent to the element. Behaviour of
            this function is determined by the properties of the
            element, as such there is no guarantee the exact string
            will be entered as is. ex: an input element that only accepts
            numbers will not accept other characters but may not raise an
            exception. Default is an empty str.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """
    try:
        find(driver, **kwargs).send_keys(text)
        logger.debug("Typed: '%s'", text)
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        find(driver, **kwargs).send_keys(text)
        logger.debug("Attempt 2 >> Typed: '%s'", text)


def write_stored_value(driver, find=_find_element, text_key='', **kwargs):
    """Send a stored string to an element in the DOM

    Execute the selenium send_keys(str) function against the locator
    that is part of the kwargs argument. If a WebDriverException
    occurs the action is attempted a second time before
    allowing the exception to be raised to the next level.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element fuinction.
        text_key:
            The str key used to store a str using ValueStore.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """
    from . import core
    text = core.read_value(text_key)
    write(driver, find=find, text=text, **kwargs)


def select_dropdown(driver, value, using, find=_find_element, **kwargs):
    """Select an option from a dropdown using text, value, or index in the DOM

    Execute the selenium Select.select_by_* function
    described by 'using' against the locator that is part of the kwargs
    argument. If a WebDriverException occurs the action is attempted
    a second time before allowing the exception to be raised to the next level.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element function.
        value:
            The DOM value to be used for selection. This can be
            the visible text (which must match the element text in
            the DOM exactly), it can be the value of the option
            element or it can be the index attribute of the desired
            option element.
        using:
            A str value that is part of the set of possible methods to
            select from a dropdown. Possible values include "text,
            value, and index" to be used to determine the
            select function from selenium.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used thus kwargs
            requires: locator.

    """
    match using:
        case 'text':
            select = Select.select_by_visible_text
            logger.debug('Selecting with visible text')
        case 'value':
            select = Select.select_by_value
            value = str(value)
            logger.debug('Selecting using option value')
        case 'index':
            select = Select.select_by_index
            logger.debug("Selecting using option index")
        case _:
            raise ValueError(f'Select method {using} is not a valid method.')

    try:
        dropdown = Select(find(driver, **kwargs))
        select(dropdown, value)
        logger.debug("Dropdown selected: '%s' -- using: '%s'", value, using)
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        dropdown = Select(find(driver, **kwargs))
        select(dropdown, value)
        logger.debug("Attempt 2 >> Dropdown selected: '%s' -- using: '%s'",
                     value, using)


def clear(driver, find=_find_element, **kwargs):
    """Clear the value of a text input element in the DOM

    Execute the selenium clear function against the locator
    that is part of the kwargs argument. If a WebDriverException
    occurs the action is attempted a second time before
    allowing the exception to be raised to the next level.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element fuinction.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """
    try:
        find(driver, **kwargs).clear()
        logger.debug("Element cleared.")
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        find(driver, **kwargs).clear()
        logger.debug("Attempt 2 >> Element cleared.")


def load_url(driver, url):
    """Load the provided URL in the current browser window

    Execute the selenium get function. Requires a fully formed
    and formatted URL.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        url:
            The url to be loaded. Must be complete and correctly formatted.
    """
    driver().get(url)
    logger.debug("Loaded url in browser: %s", url)


def load_file(driver, relative_path):
    """Load the provided file in the current browser window

    Execute the selenium get function. Requires a fa file
    path relative to the root directory.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        relative_path:
            The file path to be loaded. Must be relative to the root directory.
    """
    url = pathlib.Path(relative_path).resolve().as_uri()
    logger.debug("Looking for file to open at: %s", url)
    driver().get(url)
    logger.debug("Loaded local file in browser.")


def load_page(driver, page, url_key='url', use_local=False):
    """Load a page using the URL provided in the POM

        Execute the selenium get function against the URL or
        file path provided in the given page.

        Args:
            driver:
            The RemoteWebDriver object that is connected
            to the open browser.
            page:
            The key combination for the POM page object.
            url_key:
            The key for the url in the required environment.
            in the case of multiple URLs for the same page in
            different environments. The default value is 'url'.
            The default URL for the POM object should be 'url'.
            use_local:
            A flag that indicates if a local file should be used. In which
            case the provided url is treated like a relative file path
            instead of a web URL.
    """
    url = PageReader().get_url(*page, url_key)
    logger.debug("Read url from POM: %s", url)
    if (use_local):
        load_file(driver, url)
    else:
        load_url(driver, url)


def read_attribute(driver, attribute, find=_find_element, **kwargs):
    """Read the value of an attribute for an element in the DOM

    Execute the selenium get_attribute function against the locator
    that is part of the kwargs argument. If a WebDriverException
    occurs the action is attempted a second time before
    allowing the exception to be raised to the next level.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element fuinction.
        attribute:
            The str name of the attribute to be read from the element.
            Must match the HTML element attribute name exactly.
            Different browsers may use different spellings for the same
            values, at this time there is no automatic translation of
            attribute names so the exact value of the attribute name
            for the open browser must be supplied.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """
    try:
        attribute = str(attribute)
        attr = find(driver, **kwargs).get_attribute(attribute)
        logger.debug("Element has attribute: '%s'='%s'", attribute, attr)
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        attr = find(driver, **kwargs).get_attribute(attribute)
        logger.debug("Attempt 2 >> Element has attribute: '%s'='%s'",
                     attribute, attr)

    return attr


def read_css(driver, attribute, find=_find_element, **kwargs):
    """Read the value of a css attribute for an element in the DOM

    Execute the selenium value_of_css function against the locator
    that is part of the kwargs argument. If a WebDriverException
    occurs the action is attempted a second time before
    allowing the exception to be raised to the next level.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element fuinction.
        attribute:
            The str name of the attribute to be read from the element.
            Must match the CSS element attribute name exactly.
            Different browsers may use different spellings for the same
            values, at this time there is no automatic translation of
            attribute names so the exact value of the attribute name
            for the open browser must be supplied.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """

    try:
        attribute = str(attribute)
        prop = find(driver, **kwargs).value_of_css_property(attribute)
        logger.debug("Element has CSS property: '%s'='%s'", attribute, prop)
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        prop = find(driver, **kwargs).value_of_css_property(attribute)
        logger.debug("Attempt 2 >> Element has CSS property: '%s'='%s'",
                     attribute, prop)

    return prop


def read_text(driver, find=_find_element, **kwargs):
    """Read the text value for an element in the DOM

    Get the text value of the element with the locator
    that is part of the kwargs argument. If a WebDriverException
    occurs the action is attempted a second time before
    allowing the exception to be raised to the next level.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element fuinction.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """

    try:
        text = find(driver, **kwargs).text
        logger.info("Element has text: '%s'", text)
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        text = find(driver, **kwargs).text
        logger.info("Attempt 2 >> Element has text: '%s'", text)

    return text


def switch_frame(driver, frame, page=None, find=_find_element):
    """Change the active frame by name or element

    Execute the selenium switch_to.frame function against the locator
    provided by the frame attribute. If a WebDriverException
    occurs the action is attempted a second time before
    allowing the exception to be raised to the next level.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element fuinction.
        frame:
            The frame that should take focus. This can be either a str
            name or id of the frame or it can be a dictionary composed of 'by'
            and 'value' as a locator.

    """
    try:
        if page:
            _frame = PageReader().get_element(*page, frame)
            logger.debug("Found frame in POM.")
            switch_frame(driver, _frame, page=None, find=find)
        elif (isinstance(frame, str)):
            driver().switch_to.frame(frame)
            logger.debug("Switched active frame to: %s", frame)
        else:
            element = find(driver, page=page, **frame)
            driver().switch_to.frame(element)
            logger.debug("Switched active frame to element: %r", element)
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        if page:
            _frame = PageReader().get_element(*page, frame)
            logger.debug("Attempt 2 >> Found frame in POM.")
            switch_frame(driver, _frame, page=None, find=find)
        elif (isinstance(frame, str)):
            driver().switch_to.frame(frame)
            logger.debug("Attempt 2 >> Switched active frame to: %s", frame)
        else:
            driver().switch_to.frame(find(driver, **frame))
            logger.debug("Attempt 2 >> Switched active frame to element: %r",
                         element)

        logger.debug("Attempt 2 >> Switched active frame to: %s", frame)


def switch_window(driver, title=None, page=None):
    """Change to the next tab/window or switch to one wih a matching title.

    Execute the selenium switch_to.window function. If title
    is not given then switch to the next tab/window, if a str title
    is provided then all open windows/tabs are cycled through
    until one with a matching title is found.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        title:
            The title (str) of a window or tab to be switched to.
            The title must be an exact match in order for it to be
            found and switched to correctly.
    """
    # TODO: Keep track of window handles to avoid loop?
    # TODO: Handle switching from closed tabs
    cur_handle = None
    try:
        cur_handle = driver().current_window_handle
        logger.debug("Current window handle: %s -- title: %s",
                     cur_handle, driver().title)
    except NoSuchWindowException:
        logger.info(
            "Current window closed or missing. Switching to other tab/window"
            )
    if (page):
        switch_window(driver,
                      title=PageReader().get_page_title(*page),
                      page=None)
        return

    handles = driver().window_handles
    if (title is None):
        logger.info("Switching to next tab or window...")
        for handle in handles:
            # TODO: Handle switching if only 1 tab/window
            if (handle != cur_handle):
                driver().switch_to.window(handle)
                return
    elif (isinstance(title, str)):
        for handle in handles:
            if (handle == cur_handle):
                continue
            else:
                driver().switch_to.window(handle)
                if (driver().title == title):
                    return

    raise ValueError('No other window/tab with title: {}'.format(title))


def close(driver):
    """ Closes the currently open browser tab or window.

    Execute the selenium close function, any alerts
    must be handled before continuing execution. Use
    handle_alert function.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
    """
    try:
        driver().close()
        logger.info("Closed currently active tab/window.")
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        driver().close()
        logger.info("Closed currently active tab/window.")


def quit(driver):
    """ Closes the current browser session.

    Executes the Selenium quit function. By default,
    will also reset all instances related to the
    browser driver (waits, driver, etc.).

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
    """

    try:
        driver.quit()
        logger.info("Driver exited browser session.")
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
        driver.quit()
        logger.info("Driver exited browser session.")


def handle_alert(driver, handle=True, text=None, soft=True):
    """ Handle an expected browser alert.

    Utilizing the Selenium Alert class, handle an expected
    alert using the method described by handle. The soft
    parameter determines behaviour if an alert is not present.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        handle:
            How to handle the alert. Options include:
            'accept', 1 or True to accept the the alert
            and 'dismiss', 0, or False to dismiss the
            alert. A value of None will provide default
            behaviour of 'accept'
    """
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
        do_alert = Alert.accept
        logger.debug("Handle alert using Alert.accept()")
    else:
        do_alert = Alert.dismiss
        logger.debug("Handle alert using Alert.dismiss()")

    try:
        alert = driver().switch_to.alert
        if text and isinstance(text, str):
            logger.info("Sending text to alert prompt: %s", text)
            alert.send_keys(text)
        do_alert(alert)
    except NoAlertPresentException as na:
        if not soft:
            raise TassHardAssertionError(
                "No Alert was present. Ending Execution.", na
                )
        else:
            raise TassSoftAssertionError(
                "No Alert was present. Continuing execution.", na
                )
    except WebDriverException as e:
        logger.error("Something went wrong, %s", e)
        raise e


def screenshot(driver,
               name="screenshot",
               locator=None,
               find=_find_element,
               **kwargs):
    screenshotsfldr = pathlib.Path("screenshots").resolve()
    # Sort png by browser config
    driverfldr = [driver.os, driver.name, driver.version]
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

    try:
        if locator:
            status = find(driver, locator, **kwargs).screenshot(out)
        else:
            status = driver().save_screenshot(out)
    except WebDriverException as e:
        logger.warning("Something went wrong, %s -- Trying again", e)
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
def _fail(soft, message, exception=None, *args):
    if (soft):
        raise TassSoftAssertionError(
                "Soft Assertion failed: " + message,
                exception, *args)
    else:
        raise TassHardAssertionError(
                "Hard Assertion failed: " + message,
                exception, *args)


def assert_page_is_open(driver, page=None, find=_find_element,
                        soft=False, page_id=None):
    """Assert the given page is open using the described method

    Assert that the given page is open using one of the pre-defined methods.
    'element' checks for the presence of a given element.
    'title' checks for the given title.
    'url' checks for the given url.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element function.
        method:
            The str representation of the desired method.
            Value must match one of the predefined methods
            given above.

    """
    def _element(driver, find, element, page, soft):
        ele = None
        try:
            ele = find(driver, element, page=page)
            logger.debug("Element: %s found, page is open.", element)
        except WebDriverException:
            try:
                ele = find(driver, element, page=page)
                logger.debug("Attempt 2 >> Element: %s found, page is open.",
                             element)
            except WebDriverException as e:
                logger.warning('Exception raised: %s', e)
                _fail(soft, 'WebDriver exception raised', exception=e)

        logger.info("Element found. Page is open")

        if (ele is None):
            _fail(soft,
                  'Element {identifier} not found. Page is not open')

    def _title(driver, find, title, soft):
        if (driver().title != title):
            ele = None
            ele_title = {"by": "xpath", "value": f"//title[text()='{title}']"}
            try:
                ele = find(driver, ele_title, page=page)
                logger.debug("Element: %s found, page is open.", ele_title)
            except WebDriverException:
                try:
                    ele = find(driver, ele_title, page=page)
                    logger.debug(
                        "Attempt 2 >> Element: %s found, page is open.",
                        ele_title
                        )
                except WebDriverException as e:
                    logger.warning('Exception raised: %s', e)
            if not ele:
                _fail(soft,
                      'Expected title not found. Page is not open')

        logger.info("Found expected title. Page is open")

    def _url(driver, url, soft):
        logger.info('Current url: %s', driver().current_url)
        if (driver().current_url != url):
            _fail(soft,
                  'Expected url not open. Page is not open')

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


def assert_contains_text(driver, text, find=_find_element,
                         soft=False, exact=False, **kwargs):
    """Assert the given text is displayed in the element.
       Can be soft, or hard check.

    Using the WebElement text attribute, confirm that the specified element
    contains the text fragment provided.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        text:
            The complete text or a text fragment that
            should be in the given element
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element function.

    """
    actual_text = None
    try:
        actual_text = read_text(driver, find, **kwargs)
        logger.info("Element contains text: %s", actual_text)
        if exact and text != actual_text:
            _fail(soft, "assert_text_contains, text is not exact match.")
        elif text not in actual_text:
            _fail(soft, "assert_text_contains, text is not displayed.")
        else:
            logger.info("Element contains text: %s", text)
    except WebDriverException as e:
        logger.debug("Driver reporting error. %r", kwargs)
        if (soft):
            raise TassSoftAssertionError(
                '''Soft Assertion failed: assert_contains_text
                -> Element does not contain given text.''',
                e, *kwargs)
        else:
            raise TassHardAssertionError(
                '''Hard Assertion failed: assert_contains_text
                ->  Element does not contain given text.''',
                e, *kwargs)


def assert_displayed(driver, find=_find_element, soft=False, **kwargs):
    """Assert the given element is displayed. Can be a soft or hard check

    Execute the selenium is_displayed function against the locator
    provided. Then return true if it is displayed.
    If a WebDriverException occurs the action is attempted a
    second time before allowing the exception to be raised to the next level.

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
        if (_is_displayed(driver, find=find, **kwargs)):
            logger.info("Element is displayed.")
            return
        else:
            _fail(soft, "assert_displayed Element is not displayed.")
    except WebDriverException as e:
        logger.debug("Driver reporting error. %r", kwargs)
        if (soft):
            raise TassSoftAssertionError(
                '''Soft Assertion failed: assert_displayed
                -> Element is not displayed.''',
                e, *kwargs)
        else:
            raise TassHardAssertionError(
                '''Hard Assertion failed: assert_displayed
                ->  Element is not displayed.''',
                e, *kwargs)


def assert_not_displayed(driver, find=_find_element, soft=False, **kwargs):
    """Assert the given element is not displayed. Can be a soft of hard check

    Execute the selenium is_displayed function against the locator
    provided. Then return true if it is not displayed.
    If a WebDriverException occurs the action is attempted a
    second time before allowing the exception to be raised to the next level.

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
        if not (_is_displayed(driver, find=find, **kwargs)):
            logger.info("Element is not displayed.")
            return
        elif (soft):
            raise TassSoftAssertionError(
                '''Soft Assertion failed: assert_not_displayed
                -> Element is displayed.''',
                *kwargs)
        else:
            raise TassHardAssertionError(
                '''Hard Assertion failed: assert_not_displayed
                ->  Element is displayed.''',
                *kwargs)
    except WebDriverException as e:
        if (soft):
            logger.debug("Driver reporting error. %r", kwargs)
            raise TassSoftAssertionError(
                '''Soft Assertion failed: assert_not_displayed
                ->  Element is displayed.''',
                e, *kwargs)
        else:
            raise TassHardAssertionError(
                '''Hard Assertion failed: assert_not_displayed
                ->  Element is displayed.''',
                e, *kwargs)


def assert_attribute_contains_value(driver, attribute, value,
                                    find=_find_element, soft=False,
                                    exact=False, **kwargs):
    actual_value = None
    try:
        actual_value = read_attribute(driver, attribute, find, **kwargs)
        logger.info("Element contains attribute: %s", actual_value)
        if exact and value != actual_value:
            _fail(soft,
                  ("assert_attribute_contains, "
                   "attribute is not exact match. {%s=%s}"),
                  attribute, value)
        elif value not in actual_value:
            _fail(soft,
                  ("assert_attribute_contains, "
                   "attribute does not match. {%s=%s}"),
                  attribute, value)
        else:
            logger.info("Element contains attribute: %s with value: %s",
                        attribute, value)
    except WebDriverException as e:
        logger.debug("Driver reporting error. %r", kwargs)
        if (soft):
            raise TassSoftAssertionError(
                '''Soft Assertion failed: assert_attribute_contains_value
                -> Element attribute does not contain given value.''',
                e, *kwargs)
        else:
            raise TassHardAssertionError(
                '''Hard Assertion failed: assert_attribute_contains_value
                ->  Element attribute does not contain given value.''',
                e, *kwargs)
