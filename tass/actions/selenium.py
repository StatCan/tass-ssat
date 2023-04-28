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
    try:
        find(driver, **kwargs).click()
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        find(driver, **kwargs).click()


def type(driver, find=_find_element, text='', **kwargs):
    try:
        find(driver, **kwargs).send_keys(text)
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        find(driver, **kwargs).send_keys(text)


def clear(driver, find=_find_element, **kwargs):
    try:
        find(driver, **kwargs).clear()
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        find(driver, **kwargs).clear()


def load_url(driver, url=''):
    driver.get(url)


def load_file(driver, relative_path=''):
    url = os.path.join(pathlib.Path().resolve(), relative_path)
    driver.get('file://' + url)


def read_attribute(driver, find=_find_element, attribute='', **kwargs):
    try:
        return find(driver, **kwargs).get_attribute(attribute)
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        return find(driver, **kwargs).get_attribute(attribute)


def read_css(driver, find=_find_element, attribute='', **kwargs):
    try:
        return find(driver, **kwargs).value_of_css_property(attribute)
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        return find(driver, **kwargs).value_of_css_property(attribute)


def switch_frame(driver, find=_find_element, frame=None):
    try:
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
