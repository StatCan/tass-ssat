from ...log.logging import getLogger
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import WebDriverException



logger = getLogger(__name__)


def _perform(driver, **kwargs):
    logger.info("Performing chained steps.")
    driver.chain().perform()


def _reset(driver, **kwargs):
    driver.chain().reset_actions()
    logger.info("Chained steps reset.")


def _click(driver, find, locator, **kwargs):
    ele = None
    if locator:
        ele = find(driver, locator, **kwargs)

    logger.info("Click on element: %s added to Action Chain", locator)
    driver.chain().click(ele)


def _write(driver, find, locator, text, **kwargs):
    ele = None
    if locator:
        ele = find(driver, locator, **kwargs)

    if ele:
        logger.info(
            "Sending '%s' to element: %s added to Action Chain",
            text,
            locator
            )
        driver.chain().send_keys_to_element(ele, text)
    else:
        logger.info("Sending text: %s added to Action Chain", text)
        driver.chain().send_keys(text)


def _move_mouse(driver, find,
               locator,
               xoffset,
               yoffset,
               **kwargs):
    ele = None
    if locator:
        ele = find(driver, locator, **kwargs)


    if (xoffset or yoffset) and ele:
        # Offset and element have been provided
        # Move pointer to offset from element origin
        logger.info(
            ("Moving mouse pointer to element:"
             "%s with offset: %s,%s added to Action Chain."),
            locator, xoffset, yoffset)
        driver.chain().move_to_element_with_offset(ele, xoffset, yoffset)
    elif ele:
        # No offset is provided
        # Move pointer to element
        logger.info(
            "Moving mouse pointer to element: %s added to Action Chain",
            locator)
        driver.chain().move_to_element(ele)
    else:
        # No target element provided
        # Move pointer by offset.
        logger.info("Moving mouse pointer by offset: %s,%s", xoffset, yoffset)
        driver.chain().move_by_offset(xoffset, yoffset)


def _drag_and_drop(driver, find, locator, target,
                  xoffset, yoffset, **kwargs):
    source = find(driver, locator, **kwargs)

    if not target:
        # No target element provided
        # Drag and Drop using offset
        logger.info("Drag: %s and drop by offset: %s,%s added to Action Chain",
                    locator, xoffset, yoffset)
        driver.chain().drag_and_drop_by_offset(source, xoffset, yoffset)
    else:
        # Target element has been provided
        # Drag and drop on target element
        try:
            ele = find(driver, target, **kwargs)
        except WebDriverException as e:
            logger.warning("Something went wrong: %s -- Trying again", e)
            ele = find(driver, target, **kwargs)
        logger.info(
            "Drag: %s and drop at: %s added to Action Chain", locator, target)
        driver.chain().drag_and_drop(source, ele)


def _scroll(driver, find, locator, deltax, deltay,
           xoffset, yoffset, **kwargs):
    origin = None
    ele = None

    if locator:
        ele = find(driver, locator, **kwargs)


    # Set origin point, if there is one.
    # Determined by the presence of an offset.
    if (xoffset is not None or yoffset is not None
       or deltax or deltay) and ele:
        # Both an element and offset is provided
        # Scroll by delta amount from element offset origin
        logger.info("Element: %s with offset: %s,%s set as origin",
                    locator, xoffset, yoffset)
        xoffset = xoffset or 0  # Ensure the value is not None
        yoffset = yoffset or 0
        origin = ScrollOrigin.from_element(ele, xoffset, yoffset)
    elif xoffset is not None or yoffset is not None:
        # Only an offset is provided
        # Origin is assumed to be viewport
        xoffset = xoffset or 0  # Ensure the value is not None
        yoffset = yoffset or 0
        logger.info(
            "Top of page with offset: %s,%s set as origin", xoffset, yoffset)
        origin = ScrollOrigin.from_viewport(xoffset, yoffset)

    if origin:
        logger.info(
            "Scroll from origin by: %s,%s added to Action Chain",
            deltax, deltay)
        driver.chain().scroll_from_origin(origin, deltax, deltay)
    elif ele:
        logger.info(
            "Scroll element: %s into view added to Action Chain", locator)
        driver.chain().scroll_to_element(ele)
    else:
        logger.info(
            "Scroll page by: %s,%s added to Action Chain", deltax, deltay)
        driver.chain().scroll_by_amount(deltax, deltay)
