import pathlib
import os
from selenium.common.exceptions import WebDriverException


def click(driver, *, element=None):
    try:
        _find_element(driver, element).click()
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        _find_element(driver, element).click()


def type(driver, *, element=None, text=''):
    try:
        _find_element(driver, element).send_keys(text)
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        _find_element(driver, element).send_keys(text)


def load_url(driver, *, url=''):
    driver.get(url)


def load_file(driver, *, relative_path=''):
    url = os.path.join(pathlib.Path().resolve(), relative_path)
    driver.get('file://' + url)


def read_attribute(driver, *, element=None, attribute=''):
    try:
        return _find_element(driver, element).get_attribute(attribute)

    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        return _find_element(driver, element).get_attribute(attribute)
       


def read_css(driver, *, element=None, attribute=''):
    try:
        return _find_element(driver, element).value_of_css_property(attribute)
    except WebDriverException:
        print("Exception: ", e, " trying again")
        return _find_element(driver, element).get_attribute(attribute)
        


def _find_element(driver, element):
    return driver.find_element(*element)
