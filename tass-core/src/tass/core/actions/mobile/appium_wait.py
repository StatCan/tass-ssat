from ...log.logging import getLogger
from ..browser import selenium_wait as selwait

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
    selwait.wait_element_clickable(driver, locator,
                                   locator_args=locator_args,
                                   action=action, **kwargs)


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
    selwait.wait_element_visible(driver, locator,
                                 locator_args=locator_args,
                                 action=action, **kwargs)
