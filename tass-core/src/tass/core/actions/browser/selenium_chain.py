from ...log.logging import getLogger
from ...registry import SeleniumBroker, SeleniumChainBroker
from ..impl import _selenium_chain as selchain
from selenium.common.exceptions import WebDriverException

#  For additional documentation, see selenium docs:
#  https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html


logger = getLogger(__name__)


@SeleniumBroker.command
@SeleniumChainBroker.command
def perform(driver, **kwargs):
    """Perform all collected actions.

    Execute all selenium Action Chain actions
    that are currenty queued.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
    """
    selchain._perform(driver, **kwargs)


@SeleniumBroker.command
@SeleniumChainBroker.command
def reset(driver, **kwargs):
    """Reset stored actions in the Action Chain

    Remove all actions that are currently queued. Action Chain
    will be ready to create new queue.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.

    """
    selchain._reset(driver, **kwargs)


# To prevent command collision
# Calling chain commands from selenium namespace
# Must be preceeded by "chain_"
@SeleniumBroker.command(name="chain_click")
@SeleniumBroker.find_with(finder="find_element")
@SeleniumChainBroker.command
@SeleniumChainBroker.find_with(finder="find_element")
def click(driver, *, find, locator=None, **kwargs):
    """Add a click action to the action queue.

    Add a click action to the action queue. If a locator is
    provided, the click will target the centre of the found
    WebElement. Otherwise, the click will originate from
    the current mouse pointer location.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        locator:
            The element key to find, or the by,value pair
            to locate the WebElement in question.
        kwargs:
            Additional values to be used when locating a web element.

    """
    selchain._click(driver, find, locator, **kwargs)


@SeleniumBroker.command(name="chain_write")
@SeleniumBroker.find_with(finder="find_element")
@SeleniumChainBroker.command
@SeleniumChainBroker.find_with(finder="find_element")
def write(driver, *, find, locator=None, text='', **kwargs):
    """Add a send_keys action to the action queue.

    Add a send_keys action to the action queue. If a locator is
    provided, the send_keys_to_element will be used
    instead.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        locator:
            The element key to find, or the by,value pair
            to locate the WebElement in question.
        text:
            The text to send to the given element
        kwargs:
            Additional values to be used when locating a web element.

    """
    selchain._write(driver, find, locator, text, **kwargs)


@SeleniumBroker.command(name="chain_move_mouse")
@SeleniumBroker.find_with(finder="find_element")
@SeleniumChainBroker.command
@SeleniumChainBroker.find_with(finder="find_element")
def move_mouse(driver, find,
               locator=None,
               xoffset=0,
               yoffset=0,
               **kwargs):
    """Move the mouse pointer to the designated location.

    Add a move_mouse action to the Action Chain queue. Providing an
    offset and an element will move the mouse pointer to the given element
    adjusted by the offset provided. If only an element is provided, or the
    offset is 0,0 then the mouse pointer will be moved to the centre
    of the given element. If only an offset is given then the mouse pointer
    will be moved from it's current position by the given offset values.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        locator:
            The element key to find, or the by,value pair
            to locate the WebElement in question.
        xoffset:
            X offset to move to, as a positive or negative integer.
        yoffset:
            Y offset to move to, as a positive or negative integer.
        kwargs:
            Additional values to be used when locating a web element.
    """

    selchain._move_mouse(driver, find, locator,
                         xoffset, yoffset, **kwargs)


@SeleniumBroker.command(name="chain_drag_and_drop")
@SeleniumBroker.find_with(finder="find_element")
@SeleniumChainBroker.command
@SeleniumChainBroker.find_with(finder="find_element")
def drag_and_drop(driver, *, find, locator, target=None,
                  xoffset=0, yoffset=0, **kwargs):
    """Drag element and drop.

    Add a drag and drop action to the Action Chains queue.
    The element found by the locator will be dragged to
    the element located by target if provided. Otherwise
    will drag the element by the given offset and drop.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        locator:
            The element key to find, or the by,value pair
            to locate the WebElement in question. Element
            to be targeted by the "click and drag" function.
        target:
            The element key to find, or the by,value pair
            to locate the WebElement in question. Element
            to be targeted by the "drop" function.
        xoffset:
            X offset to move to, as a positive or negative integer.
        yoffset:
            Y offset to move to, as a positive or negative integer.
        kwargs:
            Additional values to be used when locating a web element.
    """
    selchain._drag_and_drop(driver, find,
                            locator, target,
                            xoffset, yoffset,
                            **kwargs)


@SeleniumBroker.command(name="chain_scroll")
@SeleniumBroker.find_with(finder="find_element")
@SeleniumChainBroker.command
@SeleniumChainBroker.find_with(finder="find_element")
def scroll(driver, find, locator=None, deltax=0, deltay=0,
           xoffset=None, yoffset=None, **kwargs):
    """Scroll the open page.

    Add a scroll page action to the Action Chains queue.
    When an offset and a locator are provided the origin
    point of the scroll will be set to the centre of
    the located element adjusted by the offset. If no
    element is provided, the origin point is assumed to
    be the top left of the viewport adjusted by the offset.

    The page will be scrolled by the amount indicated by the
    delta values from the above origin point if applicable.

    When an element is provided without an offset, the element
    is scrolled into the viwport, with element at the bottom,
    ignoring the delta values.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
        locator:
            The element key to find, or the by,value pair
            to locate the WebElement in question.
        deltax:
            Distance along X axis to scroll using the wheel.
            A negative value scrolls left.
        deltay:
            Distance along Y axis to scroll using the wheel.
            A negative value scrolls up.
        xoffset:
            X offset to move to, as a positive or negative integer.
        yoffset:
            Y offset to move to, as a positive or negative integer.
        kwargs:
            Additional values to be used when locating a web element.

    """
    selchain._scroll(driver, find,
                     locator,
                     deltax, deltay,
                     xoffset, yoffset,
                     **kwargs)
