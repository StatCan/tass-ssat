def click(driver, element):
    _find_element(driver, element).click()


def type(driver, element, text):
    _find_element(driver, element).send_keys(text)


def load_url(driver, url):
    driver.get(url)


def read_attribute(driver, element, attribute):
    return _find_element(driver, element).get_attribute(attribute)


def _find_element(driver, element):
    return driver.find_element(element['by'], element['locator'])
