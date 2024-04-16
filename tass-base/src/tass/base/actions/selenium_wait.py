import selenium.webdriver.support.expected_conditions as EC
from ..log.logging import getLogger
from . import selenium as sel

logger = getLogger(__name__)


def wait_element_clickable(driver, locator,
                           locator_args=None,
                           action=None, **kwargs):
    """Wait until element is visible and enabled.

    Execute the specified action after waiting for the element
    found with the designated locator to be visible
    and enabled. Will timeout if waiting for longer than the
    given time or the default wait time if None. If no action is
    provided, execution will resume after condition is met.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        locator:
            The locator object or the POM key for an element.
        action:
            An array containing 2 elements. The first being the
            location of the action, the second being the name of
            the action to be taken after the condition is met.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
    """
    def _wait(driver, locator, locator_args=None, page=None, time=None):
        mark = tuple(sel.locate(page, locator, locator_args).values())
        logger.debug("Waiting for element to be clickable: %s", mark)
        return driver.wait_until(EC.element_to_be_clickable, time=time,
                                 mark=mark)

    if (action is None):
        logger.info("Waiting for element before continuing...")
        _wait(driver, locator, locator_args, **kwargs)
    else:
        logger.info("Waiting for element before selenium action: %s",
                    action[1])
        # TODO: Rework this to perform ANY action not just selenium
        # TODO: Alternate: Create generic wait until condition in core?
        getattr(sel, action[1])(driver,
                                find=_wait,
                                locator=locator,
                                **kwargs)


def wait_element_visible(driver, locator,
                         locator_args=None,
                         action=None, **kwargs):
    """Wait until element is visible.

    Execute the specified action after waiting for the element
    found with the designated locator to be visible.
    Will timeout if waiting for longer than the
    given time or the default wait time if None. If no action is
    provided, execution will resume after condition is met.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        locator:
            The locator object or the POM key for an element.
        action:
            An array containing 2 elements. The first being the
            location of the action, the second being the name of
            the action to be taken after the condition is met.
        **kwargs:
            Dictionary containing additional parameters. Contents
            of the dictionary will vary based on the find function used.
    """
    def _wait(driver, locator, locator_args=None, time=None, page=None):
        mark = tuple(sel.locate(page, locator, locator_args).values())
        logger.debug("Waiting for element to be visible: %s", mark)
        return driver.wait_until(EC.visibility_of_element_located, time=time,
                                 locator=mark)

    if (action is None):
        logger.info("Waiting for element before continuing...")
        _wait(driver, locator, locator_args, **kwargs)
    else:
        # TODO: Rework this to perform ANY action not just selenium
        # TODO: Alternate: Create generic wait until condition in core?
        logger.info("Waiting for element before selenium action: %s",
                    action[1])
        getattr(sel, action[1])(driver,
                                find=_wait,
                                locator=locator,
                                **kwargs)
