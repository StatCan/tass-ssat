import pathlib
from tass.core.page_reader import PageReader
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select
from tass.exceptions.assertion_errors import TassHardAssertionError
from tass.exceptions.assertion_errors import TassSoftAssertionError


def locate(page, locator, locator_args):
    print(locator)
    if (isinstance(locator, str)):
        _loc = PageReader().get_element(*page, locator)
    elif isinstance(locator, dict):
        _loc = locator
    else:
        msg = "Locator type not supported. Type: {}".format(type(locator))
        raise TypeError(msg)

    if locator_args:
        _loc['value'] = _loc['value'].format(*locator_args)

    return _loc


def _find_element(driver, locator, locator_args=None, page=None):
    return driver.find_element(**locate(page, locator, locator_args))


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
    from tass.actions.core import read_value
    text = read_value(text_key)
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
            or the default _find_element fuinction.
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
            By default, _find_element is used and thus kwargs
            requires: locator.

    """
    match using:
        case 'text':
            select = Select.select_by_visible_text
        case 'value':
            select = Select.select_by_value
        case 'index':
            select = Select.select_by_index
        case _:
            raise ValueError('Select method {using} is not a valid method.')

    try:
        dropdown = Select(find(driver, **kwargs))
        select(dropdown, value)
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        dropdown = Select(find(driver, **kwargs))
        select(dropdown, value)


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
    url = pathlib.Path(relative_path).resolve().as_uri()
    driver.get(url)


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
        # TODO: if/else logic needs to be revisited for POM implementation.
        if (isinstance(frame, str)):
            driver.switch_to.frame(frame)
        else:
            driver.switch_to.frame(find(driver, page=page, **frame))
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        if (isinstance(frame, str)):
            driver.switch_to.frame(frame)
        else:
            driver.switch_to.frame(find(driver, **frame))


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
    cur_handle = driver.current_window_handle
    if (title is None):
        for handle in driver.window_handles:
            if (handle != cur_handle):
                driver.switch_to.window(handle)
                return
    elif (page is not None):
        switch_window(driver,
                      title=PageReader().get_page_title(*page))
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
            or the default _find_element fuinction.
        method:
            The str representation of the desired method.
            Value must match one of the predefined methods
            given above.

    """
    def _element(driver, find, element, page, soft):
        ele = None
        try:
            ele = find(driver, element, page=page)
        except WebDriverException:
            try:
                ele = find(driver, element, page=page)
            except WebDriverException as e:
                print('Exception raised: {}'.format(e))
                _fail(soft, 'WebDriver exception raised', exception=e)

        if (ele is None):
            _fail(soft,
                  'Element {identifier} not found. Page is not open')

    def _title(driver, title, soft):
        if (driver.title != title):
            _fail(soft,
                  'Expected title not found. Page is not open')

    def _url(driver, url, soft):
        if (driver.current_url != url):
            _fail(soft,
                  'Expected url not open. Page is not open')
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
                title = PageReader() \
                    .get_page_title(*page, default=page_id['identifier'])
                _title(driver, title, soft)
            case 'url':
                url = PageReader() \
                    .get_url(*page, default=page_id['identifier'])
                _url(driver, url, soft)
            case _:
                raise ValueError(
                    "Method, {page_id.get('method', 'element')} not supported")
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
                _title(driver, title, soft)
            case 'url':
                url = page_id['identifier']
                _url(driver, url, soft)
            case _:
                raise ValueError(
                    "Method, {page_id.get('method', 'element')} not supported")
    elif (page is None and page_id is None):
        raise ValueError('Either page or page_id must not be None')


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
        else:
            _fail(soft, "assert_displayed Element is not displayed.")
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
