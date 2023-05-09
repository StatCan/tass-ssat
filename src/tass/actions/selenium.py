import pathlib
import os
from selenium.common.exceptions import WebDriverException
from tass.exceptions.assertion_errors import TassHardAssertionError
from tass.exceptions.assertion_errors import TassSoftAssertionError


def _find_element(driver, locator):
    return driver.find_element(**locator)


def _is_displayed(driver, find=_find_element, **kwargs):
    try:
        return find(driver, **kwargs).is_displayed()
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        return find(driver, **kwargs).is_displayed()


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
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        find(driver, **kwargs).click()


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
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        find(driver, **kwargs).send_keys(text)


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
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        find(driver, **kwargs).clear()


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

    driver.get(url)


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
    url = os.path.join(pathlib.Path().resolve(), relative_path)
    driver.get('file://' + url)


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
        return find(driver, **kwargs).get_attribute(attribute)
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        return find(driver, **kwargs).get_attribute(attribute)


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
        return find(driver, **kwargs).value_of_css_property(attribute)
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        return find(driver, **kwargs).value_of_css_property(attribute)


def switch_frame(driver, frame, find=_find_element):
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
        # TODO: if/else logic needs to be revisited for POM implementation.
        if (isinstance(frame, str)):
            driver.switch_to.frame(frame)
        else:
            driver.switch_to.frame(find(driver, **frame))
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        if (isinstance(frame, str)):
            driver.switch_to.frame(frame)
        else:
            driver.switch_to.frame(find(driver, **frame))


def switch_window(driver, title=None):
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
    cur_handle = driver.current_window_handle
    if (title is None):
        for handle in driver.window_handles:
            if (handle != cur_handle):
                driver.switch_to.window(handle)
                return
    elif (isinstance(title, str)):
        for handle in driver.window_handles:
            if (handle == cur_handle):
                continue
            else:
                driver.switch_to.window(handle)
                if (driver.title == title):
                    return
    raise ValueError('No window with title: {}'.format(title))


# / / / / / / / Assertions / / / / / / /
def assert_displayed(driver, find=_find_element, soft=False, **kwargs):
    """Assert the given element is displayed. Can be a soft of hard check

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
            return
        elif (soft):
            raise TassSoftAssertionError(
                '''Soft Assertion failed: assert_displayed
                -> Element is not displayed.''',
                *kwargs)
        else:
            raise TassHardAssertionError(
                '''Hard Assertion failed: assert_displayed
                -> Element is not displayed.''',
                *kwargs)
    except WebDriverException as e:
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
            raise TassSoftAssertionError(
                '''Soft Assertion failed: assert_not_displayed
                ->  Element is displayed.''',
                e, *kwargs)
        else:
            raise TassHardAssertionError(
                '''Hard Assertion failed: assert_not_displayed
                ->  Element is displayed.''',
                e, *kwargs)
