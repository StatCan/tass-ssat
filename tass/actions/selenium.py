import pathlib
import os
from selenium.common.exceptions import WebDriverException

def _find_element(driver, element):
    return driver.find_element(**element)


def click(driver, find=_find_element, element=None):
    try:
        find(driver, element).click()
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        find(driver, element).click()


def type(driver, find=_find_element, element=None, text=''):
    try:
        find(driver, element).send_keys(text)
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        find(driver, element).send_keys(text)


def load_url(driver, url=''):
    driver.get(url)


def load_file(driver, relative_path=''):
    url = os.path.join(pathlib.Path().resolve(), relative_path)
    driver.get('file://' + url)


def read_attribute(driver, find=_find_element, element=None, attribute=''):
    try:
        return find(driver, element).get_attribute(attribute)

    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        return find(driver, element).get_attribute(attribute)


def read_css(driver, find=_find_element, element=None, attribute=''):
    try:
        return find(driver, element).value_of_css_property(attribute)
    except WebDriverException as e:
        print("Exception: ", e, " trying again")
        return find(driver, element).value_of_css_property(attribute)
