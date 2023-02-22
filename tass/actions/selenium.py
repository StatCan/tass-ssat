import pathlib
import os
from selenium.common.exceptions import WebDriverException


def click(driver, *, element=None):
    try:
        _find_element(driver, element).click()
    except WebDriverException:
        print("Exception, trying again")
        _find_element(driver, element).click()


def type(driver, *, element=None, text=''):
    try:
        _find_element(driver, element).send_keys(text)
    except WebDriverException:
        print("Exception, trying again")
        _find_element(driver, element).send_keys(text)


def load_url(driver, *, url=''):
    driver.get(url)


def load_file(driver, *, file_name=''):
    url = os.path.join(pathlib.Path().resolve(), 'pages', file_name)
    print(url)
    driver.get('file://' + url)


def read_attribute(driver, *, element=None, attribute=''):
    try:
        attr = _find_element(driver, element).get_attribute(attribute)
        print(attr)
        return attr
    except WebDriverException:
        print("Exception, trying again")
        attr = _find_element(driver, element).get_attribute(attribute)
        print(attr)
        return attr


def read_css(driver, *, element=None, attribute=''):
    try:
        attr = _find_element(driver, element).value_of_css_property(attribute)
        print(attr)
        return attr
    except WebDriverException:
        attr = _find_element(driver, element).get_attribute(attribute)
        print(attr)
        return attr


def _find_element(driver, element):
    return driver.find_element(*element)
