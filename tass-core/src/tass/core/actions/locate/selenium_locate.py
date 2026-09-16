import selenium.webdriver.support.expected_conditions as EC
from . import locate, logger
from tass.core.registry import SeleniumFinders


@SeleniumFinders.finder(name="find_element")
def find_element(driver, locator, locator_args=None, page=None):
    logger.debug("Searching for element...")
    return driver().find_element(**locate(page, locator, locator_args))

@SeleniumFinders.finder(name="wait_element_visible")
def _wait_element_visible(driver, locator, locator_args=None, time=None, page=None):
        mark = tuple(locate(page, locator, locator_args).values())
        logger.debug("Waiting for element to be visible: %s", mark)
        return driver.wait_until(EC.visibility_of_element_located, time=time,
                                 locator=mark)


@SeleniumFinders.finder(name="wait_element_clickable")
def _wait_element_clickable(driver, locator, locator_args=None, page=None, time=None):
        mark = tuple(locate(page, locator, locator_args).values())
        logger.debug("Waiting for element to be clickable: %s", mark)
        return driver.wait_until(EC.element_to_be_clickable, time=time,
                                 mark=mark)