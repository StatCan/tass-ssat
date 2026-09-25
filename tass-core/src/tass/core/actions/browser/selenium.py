import pathlib
from datetime import datetime
from selenium.common.exceptions import (WebDriverException,
                                        NoSuchWindowException,
                                        NoAlertPresentException)
from ...tools.page_reader import PageReader
from ...exceptions.assertion_errors import TassHardAssertionError
from ...exceptions.assertion_errors import TassSoftAssertionError
from ...log.logging import getLogger
from ...registry import SeleniumBroker
from ..impl import selcmds

#  For additional documentation, see selenium docs:
#  https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html


logger = getLogger(__name__)

RETRY_EXC = [WebDriverException]

@SeleniumBroker.command(retry_exc=RETRY_EXC)
@SeleniumBroker.find_with(finder="find_element")
def click(driver, *, find, **kwargs):
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
    return selcmds._click(driver, find, **kwargs)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
@SeleniumBroker.find_with(finder="find_element")
def write(driver, *, find, text='', **kwargs):
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
    return selcmds._write(driver, find, text, **kwargs)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
@SeleniumBroker.find_with(finder="find_element")
def write_stored_value(driver, *, find, text_key='', **kwargs):
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
    return selcmds._write_stored_value(driver, find, text_key, **kwargs)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
@SeleniumBroker.find_with(finder="find_element")
def select_dropdown(driver, *, find, value, using, **kwargs):
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
    return selcmds._select_dropdown(driver, find, value, using, **kwargs)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
@SeleniumBroker.find_with(finder="find_element")
def clear(driver, *, find, **kwargs):
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
    return selcmds._clear(driver, find, **kwargs)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
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
    return selcmds._load_url(driver, url)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
def load_file(driver, relative_path):
    """Load the provided file in the current browser window

    Execute the selenium get function. Requires a file
    path relative to the root directory.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        relative_path:
            The file path to be loaded. Must be relative to the root directory.
    """
    return selcmds._load_file(driver, relative_path)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
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
    return selcmds._load_page(driver, page, url_key, use_local)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
@SeleniumBroker.find_with(finder="find_element")
def read_attribute(driver, *, find, attribute, **kwargs):
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
    return selcmds._read_attribute(driver, find, attribute, **kwargs)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
@SeleniumBroker.find_with(finder="find_element")
def read_css(driver, *, find, attribute, **kwargs):
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

    return selcmds._read_css(driver, find, attribute, **kwargs)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
@SeleniumBroker.find_with(finder="find_element")
def read_text(driver, *, find, **kwargs):
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

    return selcmds._read_text(driver, find, **kwargs)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
@SeleniumBroker.find_with(finder="find_element")
def switch_frame(driver, *, find, frame, page=None):
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
    return selcmds._switch_frame(driver, find, frame, page)
    


@SeleniumBroker.command(retry_exc=RETRY_EXC)
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
    return selcmds._switch_window(driver, title, page)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
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
    return selcmds._close(driver)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
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

    return selcmds._quit(driver)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
def handle_alert(driver, handle=True, text=None):
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
            'accept', 1 or True to accept the alert
            and 'dismiss', 0, or False to dismiss the
            alert. A value of None will provide default
            behaviour of 'accept'
    """
    return selcmds._handle_alert(driver, handle, text)


@SeleniumBroker.command(retry_exc=RETRY_EXC)
@SeleniumBroker.find_with(finder="find_element")
def screenshot(driver,
               find,
               name="screenshot",
               locator=None,
               **kwargs):
    return selcmds._screenshot(driver, find, name, locator, **kwargs)


# / / / / / / / Assertions / / / / / / /


@SeleniumBroker.command
def assert_alert_displayed(driver, text=None, soft=False):
    """ Assert that an alert is currently displayed in the browser.

    Using the Selenium Alert class, assert that an alert is currently
    displayed in the browser. If no alert is present a
    TassSoftAssertionError or TassHardAssertionError is raised
    depending on the value of soft.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        soft:
            Boolean flag that indicates if a failed assertion
            should end execution. If True execution for the
            current test stops upon returning. If false, error is
            recorded and execution can continue. The default is False.
    """
    return selcmds._assert_alert_displayed(driver, text, soft)


@SeleniumBroker.command
@SeleniumBroker.find_with(finder="find_element")
def assert_page_is_open(driver, *, find, page=None,
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
    return selcmds._assert_page_is_open(driver, find, page, soft, page_id)


@SeleniumBroker.command
@SeleniumBroker.find_with(finder="find_element")
def assert_contains_text(driver, *, find, text,
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
    return selcmds._assert_contains_text(driver, find, text, soft, exact, **kwargs)


@SeleniumBroker.command
@SeleniumBroker.find_with(finder="find_element")
def assert_displayed(driver, *, find, soft=False, **kwargs):
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
    return selcmds._assert_displayed(driver, find, soft, **kwargs)


@SeleniumBroker.command
@SeleniumBroker.find_with(finder="find_element")
def assert_not_displayed(driver, *, find, soft=False, **kwargs):
    """Assert the given element is not displayed. Can be a soft of hard check

    Execute the selenium is_displayed function against the locator
    provided. Then return true if it is not displayed.

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
    return selcmds._assert_not_displayed(driver, find, soft, **kwargs)


@SeleniumBroker.command
@SeleniumBroker.find_with(finder="find_element")
def assert_attribute_contains_value(driver, *, find, attribute, value,
                                     soft=False,
                                    exact=False, **kwargs):
    """ Assert that the given element contains the specified
    value for the given attribute.

    Execute the Selenium read_attribute function and compare the
    actual value taken from the DOM to the given value.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        attribute:
            The name of the atribute to check within the DOM.
        value:
            The expected value of the above attribute within the DOM.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element fuinction.
        soft:
            Boolean flag that indicates if a failed assertion
            should end execution. If True execution for the
            current test stops upon returning. If false, error is
            recorded and execution can continue. The default is False.
        exact:
            Flag to determine if an exact match is needed. Useful for
            checking for a partial string value. If exact is True
            the actual value must match exactly, and if exact is
            False the actual and expected and compared using the
            "in" keyword. The default is False.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.

    """
    return selcmds._assert_attribute_contains_value(driver, find, attribute, value, soft, exact, **kwargs)
