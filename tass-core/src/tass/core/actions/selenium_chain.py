from ..log.logging import getLogger
from . import selenium as sel
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import WebDriverException

#  For additional documentation, see selenium docs:
#  https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html


logger = getLogger(__name__)


def perform(driver, **kwargs):
    """Perform all collected actions.

    Execute all selenium Action Chain actions
    that are currenty queued.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
    """
    logger.info("Performing chained steps.")
    driver.chain().perform()


def reset(driver, **kwargs):
    """Reset stored actions in the Action Chain

    Remove all actions that are currently queued. Action Chain
    will be ready to create new queue.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.

    """
    driver.chain().reset_actions()
    logger.info("Chained steps reset.")


def click(driver, locator=None, **kwargs):
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
    ele = None
    if locator:
        try:
            ele = sel._find_element(driver, locator, **kwargs)
        except WebDriverException as e:
            logger.warning("Something went wrong: %s -- Trying again", e)
            ele = sel._find_element(driver, locator, **kwargs)
    logger.info("Click on element: %s added to Action Chain", locator)
    driver.chain().click(ele)


def move_mouse(driver, locator=None,
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
    
    ele = None
    if locator:
        try:
            ele = sel._find_element(driver, locator, **kwargs)
        except WebDriverException as e:
            logger.warning("Something went wrong: %s -- Trying again", e)
            ele = sel._find_element(driver, locator, **kwargs)

    if (xoffset or yoffset) and ele:
        #  Offset and element have been provided
        #  Move pointer to offset from element origin
        logger.info("Moving mouse pointer to element: %s with offset: %s,%s added to Action Chain.",
                    locator, xoffset, yoffset)
        driver.chain().move_to_element_with_offset(ele, xoffset, yoffset)
    elif ele:
        #  No offset is provided
        #  Move pointer to element
        logger.info("Moving mouse pointer to element: %s added to Action Chain", locator)
        driver.chain().move_to_element(ele)
    else:
        #  No target element provided
        #  Move pointer by offset.
        logger.info("Moving mouse pointer by offset: %s,%s", xoffset, yoffset)
        driver.chain().move_by_offset(xoffset, yoffset)


def drag_and_drop(driver, locator, target=None, xoffset=0, yoffset=0,
                  **kwargs):
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


    try:
        source = sel._find_element(driver, locator, **kwargs)
    except WebDriverException as e:
        logger.warning("Something went wrong: %s -- Trying again", e)
        source = sel._find_element(driver, locator, **kwargs)

    if not target:
        #  No target element provided
        #  Drag and Drop using offset
        logger.info("Drag: %s and drop by offset: %s,%s added to Action Chain",
                    source, xoffset, yoffset)
        driver.chain().drag_and_drop_by_offset(locator, xoffset, yoffset)
    else:
        #  Target element has been provided
        #  Drag and drop on target element
        try:
            ele = sel._find_element(driver, target, **kwargs)
        except WebDriverException as e:
            logger.warning("Something went wrong: %s -- Trying again", e)
            ele = sel._find_element(driver, target, **kwargs)
        logger.info("Drag: %s and drop at: %s added to Action Chain", locator, target)
        driver.chain().drag_and_drop(source, ele)

def scroll(driver, locator=None, deltax=0, deltay=0, 
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
    
    origin = None
    ele = None

    if locator:
        try:
            ele = sel._find_element(driver, locator, **kwargs)
        except WebDriverException as e:
            logger.warning("Something went wrong: %s -- Trying again", e)
            ele = sel._find_element(driver, locator, **kwargs)

    #  Set origin point, if there is one.
    #  Determined by the presence of an offset.
    if (xoffset is not None or yoffset is not None) and ele:
        #  Both an element and offset is provided
        #  Scroll by delta amount from element offset origin
        logger.info("Element: %s with offset: %s,%s set as origin",
                    locator, xoffset, yoffset)
        xoffset = xoffset or 0 #  Ensure the value is not None
        yoffset = yoffset or 0 
        origin = ScrollOrigin.from_element(ele, xoffset, yoffset)
    elif xoffset is not None or yoffset is not None:
        #  Only an offset is provided
        #  Origin is assumed to be viewport
        xoffset = xoffset or 0 #  Ensure the value is not None
        yoffset = yoffset or 0
        logger.info("Top of page with offset: %s,%s set as origin", xoffset, yoffset)
        origin = ScrollOrigin.from_viewport(xoffset, yoffset)
    
    if origin:
        logger.info("Scroll from origin by: %s,%s added to Action Chain", deltax, deltay)
        driver.chain().scroll_from_origin(origin, deltax, deltay)
    elif ele:
        logger.info("Scroll element: %s into view added to Action Chain", locator)
        driver.chain().scroll_to_element(ele)
    else:
        logger.info("Scroll page by: %s,%s added to Action Chain", deltax, deltay)
        driver.chain().scroll_by_amount(deltax, deltay)

    

