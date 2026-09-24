from ...registry import AppiumBroker, AppiumWaitBroker
from ...log.logging import getLogger

logger = getLogger(__name__)
DOCS = ""


@AppiumBroker.command
@AppiumBroker.find_with(finder="wait_element_clickable")
@AppiumWaitBroker.command
@AppiumWaitBroker.find_with(finder="wait_element_clickable")
def wait_element_clickable(driver, *, find, locator,
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
    logger.warning("selenium_wait functions are deprecated and will be removed in a future version. Consider using the 'find' argument with basic selenium commands")
    logger.warning("See for details: %s", DOCS)
    if (action is None):
        logger.info("Waiting for element before continuing...")
        find(driver, locator, locator_args, **kwargs)
    else:
        logger.info("Waiting for element before selenium action: %s",
                    action[1])
        # TODO: Rework this to perform ANY action not just selenium
        # TODO: Alternate: Create generic wait until condition in core?
        return AppiumBroker.get(action[1])(driver=driver,
                                             find=find,
                                             locator=locator,
                                             locator_args=locator_args,
                                             **kwargs)


@AppiumBroker.command
@AppiumBroker.find_with(finder="wait_element_visible")
@AppiumWaitBroker.command
@AppiumWaitBroker.find_with(finder="wait_element_visible")
def wait_element_visible(driver, *, find, locator,
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
    logger.warning("selenium_wait functions are deprecated and will be removed in a future version. Consider using the 'find' argument with basic selenium commands")
    logger.warning("See for details: %s", DOCS)
    if (action is None):
        logger.info("Waiting for element before continuing...")
        find(driver, locator, locator_args, **kwargs)
    else:
        # TODO: Rework this to perform ANY action not just selenium
        # TODO: Alternate: Create generic wait until condition in core?
        logger.info("Waiting for element before selenium action: %s",
                    action[1])
        return AppiumBroker.get(action[1])(driver=driver,
                                             find=find,
                                             locator=locator,
                                             locator_args=locator_args,
                                             **kwargs)
