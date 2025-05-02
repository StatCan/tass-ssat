from ..log.logging import getLogger
from . import selenium as sel
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import WebDriverException


logger = getLogger(__name__)


def perform(driver, *args, **kwargs):
    logger.info("Performing chained steps.")
    driver.chain().perform()


def reset(driver, *args, **kwargs):
    driver.chain().reset_actions()
    logger.info("Chained steps reset.")


def click(driver, locator=None, *args, **kwargs):
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
               *args,
               **kwargs):
    
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
                  *args, **kwargs):
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
           xoffset=None, yoffset=None, *args, **kwargs):
    
    origin = None
    ele = None

    if locator:
        try:
            ele = sel._find_element(driver, locator, **kwargs)
        except WebDriverException as e:
            logger.warning("Something went wrong: %s -- Trying again", e)
            ele = sel._find_element(driver, locator, **kwargs)

    if (xoffset is not None or yoffset is not None) and ele:
        #  Both an element and offset is provided
        #  Scroll by delta amount from element offset origin
        logger.info("Element: %s with offset: %s,%s set as origin",
                    locator, xoffset, yoffset)
        origin = ScrollOrigin.from_element(ele, xoffset, yoffset)
    elif xoffset is not None or yoffset is not None:
        #  Only an offset is provided
        #  Origin is assumed to be viewport
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

    

