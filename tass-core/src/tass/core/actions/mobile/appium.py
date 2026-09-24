import pathlib
from datetime import datetime
from ..impl import _appium as app
from ...tools.page_reader import PageReader
from ...log.logging import getLogger
from ...registry import AppiumBroker
from selenium.common.exceptions import WebDriverException

#  For additional documentation, see selenium docs:
#  https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html


logger = getLogger(__name__)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
def click(driver,
          *, find,
          pointer_type=None,
          **kwargs):
    """Click an element in the DOM

    Execute the selenium click function against the locator
    that is part of the kwargs argument. If a WebDriverException
    occurs the action is attempted a second time before
    allowing the exception to be raised to the next level.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        pointer_type:
            String value for the JavaScript PointerType.
            Valid entries are: [touch, mouse, pen]
            Defaults to touch for Appium actions.
        find:
            The function to be called when attempting to locate
            an element. Must use either a explicit wait function
            or the default _find_element function.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """
    app._click(driver, find, pointer_type, **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
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
            or the default _find_element function.
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
    app._write(driver, find, text, **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
def write_stored_value(driver,
                       *, find,
                       text_key='',
                       **kwargs):
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
            or the default _find_element function.
        text_key:
            The str key used to store a str using ValueStore.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """
    app._write_stored_value(driver, find, text_key, **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
def select_dropdown(driver, *,
                    find,
                    value,
                    using,
                    **kwargs):
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
    app._select_dropdown(driver, find, value, using, **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
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
            or the default _find_element function.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """
    app._clear(driver, find, **kwargs)


@AppiumBroker.command
def load_url(driver, *, url):
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
    app._load_url(driver, url)


@AppiumBroker.command
def load_file(driver, *, relative_path):
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
    app._load_file(driver, relative_path)


@AppiumBroker.command
def load_page(driver, *, page, url_key='url', use_local=False):
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
    app._load_page(driver, page, url_key, use_local)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
def read_attribute(driver, *,
                   find,
                   attribute,
                   **kwargs):
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
            or the default _find_element function.
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
    return app._read_attribute(driver, find, attribute, **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
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
            or the default _find_element function.
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

    return app._read_css(driver, find, attribute, **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
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
            or the default _find_element function.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
            By default, _find_element is used and thus kwargs
            requires: locator.
    """

    return app._read_text(driver, find, **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
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
            or the default _find_element function.
        frame:
            The frame that should take focus. This can be either a str
            name or id of the frame or it can be a dictionary composed of 'by'
            and 'value' as a locator.

    """
    app._switch_frame(driver, find, frame, page)


@AppiumBroker.command
def switch_window(driver, *, title=None, page=None):
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
    app._switch_window(driver, title, page)


@AppiumBroker.command
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
    app._close(driver)


@AppiumBroker.command
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

    app._quit(driver)


@AppiumBroker.command
def handle_alert(driver, *, handle=True, text=None):
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
    app._handle_alert(driver, handle, text)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
def screenshot(driver, *,
               find,
               name="screenshot",
               locator=None,
               **kwargs):

    return app._screenshot(driver, find, name, locator, **kwargs)


# / / / / / / / Assertions / / / / / / /
# TODO: If the appium command only calls the selenium command, does it need to be added to the registry?
@AppiumBroker.command
def assert_alert_displayed(driver, *, text=None, soft=False):
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
    app._assert_alert_displayed(driver, text, soft)

@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
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
    app._assert_page_is_open(driver, find,
                             page, soft,
                             page_id)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
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
    app._assert_contains_text(driver, find, text,
                             soft, exact, **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
def assert_displayed(driver, *,
                     find,
                     soft=False,
                     **kwargs):
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
            or the default _find_element function.
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
    app._assert_displayed(driver, find, soft, **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
def assert_not_displayed(driver, *,
                         find,
                         soft=False,
                         **kwargs):
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
            or the default _find_element function.
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
    app._assert_not_displayed(driver, find, soft, **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="find_element")
def assert_attribute_contains_value(driver, *,
                                    find,
                                    attribute,
                                    value,
                                    soft=False,
                                    exact=False,
                                    **kwargs):
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
            or the default _find_element function.
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
    app._assert_attribute_contains_value(driver, find, attribute,
                                         value, soft,
                                        exact, **kwargs)
