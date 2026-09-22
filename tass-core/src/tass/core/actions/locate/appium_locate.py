from . import locate, logger
from tass.core.registry import AppiumFinders
import selenium.webdriver.support.expected_conditions as EC



def __hide_keyboard(driver, **kwargs):
    if driver().is_keyboard_shown():
        driver().hide_keyboard(**kwargs)
        logger.debug("Hiding keyboard...")



@AppiumFinders.finder(name="find_element")
def find_element_hide_keyboard(driver,
                                locator, *,
                                locator_args=None,
                                page=None,
                                hide_keyboard=True,
                                **kwargs):
    # Hide keyboard before locating element if True.
    # Set to False to keep keyboard open.
    if hide_keyboard:
        __hide_keyboard(driver, **kwargs)
    logger.debug("Searching for element...")
    return driver().find_element(**locate(page, locator, locator_args))


@AppiumFinders.finder(name="wait_element_visible")
def _wait_element_visible(driver, locator, *,
                          locator_args=None, time=None,
                          page=None, hide_keyboard=True,
                          **kwargs):
        mark = tuple(locate(page, locator, locator_args).values())
        logger.debug("Waiting for element to be visible: %s", mark)
        if hide_keyboard:
            __hide_keyboard(driver, **kwargs)
        return driver.wait_until(EC.visibility_of_element_located, time=time,
                                 locator=mark)


@AppiumFinders.finder(name="wait_element_clickable")
def _wait_element_clickable(driver, locator, *,
                            locator_args=None, time=None,
                            page=None, hide_keyboard=True,
                            **kwargs):
        mark = tuple(locate(page, locator, locator_args).values())
        logger.debug("Waiting for element to be clickable: %s", mark)
        if hide_keyboard:
            __hide_keyboard(driver, **kwargs)
        return driver.wait_until(EC.element_to_be_clickable, time=time,
                                 mark=mark)