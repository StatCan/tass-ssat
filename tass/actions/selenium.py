import pathlib
import os
import sys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException


def _find_element(driver, locator):
    return driver.find_element(**locator)


def _wait_for_element(driver, **kwargs):
    return driver.wait_until(**kwargs)


def wait_until(driver, until='', action='', **kwargs):
    print('-----***-----', kwargs, '-----***-----')
    kwargs.update(
        {'until_func': getattr(sys.modules[__name__], '_wait_'+until)})
    return getattr(
        sys.modules[__name__], action)(
            driver, find=_wait_for_element, **kwargs)


def click(driver, find=_find_element, **kwargs):
    try:
        print('-----***-----', kwargs, '-----***-----')
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


# Selenium waits are listed below
def _wait_css_includes(locator=[], attribute='', expected_value=''):

    def _predicate(driver):
        try:
            elem = _find_element(driver, locator)
            if (elem and
                    expected_value in elem.value_of_css_property(attribute)):
                return elem
            else:
                return False
        except StaleElementReferenceException:
            return False

    return _predicate
