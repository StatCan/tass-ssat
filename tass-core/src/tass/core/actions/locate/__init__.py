from tass.core.log.logging import getLogger
from tass.core.tools.page_reader import PageReader

logger = getLogger(__name__)



def locate(page, locator, locator_args):
    logger.debug("Locator: %s -- Args: %s", locator, locator_args)
    if (isinstance(locator, str)):
        logger.debug("Getting locator (%s) from POM: %s", locator, page)
        _loc = PageReader().get_element(*page, locator)
    elif isinstance(locator, dict):
        logger.debug("Locator provided directly...")
        _loc = locator
    else:
        msg = "Locator type not supported. Type: {}".format(type(locator))
        logger.error(msg)
        raise TypeError(msg)

    if locator_args:
        logger.debug("Filling in blanks in locator using: %s", locator_args)
        # scenario converter shold convert locator args to a list by default
        _loc['value'] = _loc['value'].format(*locator_args)

    logger.debug("Using locator: %s", _loc)
    return _loc