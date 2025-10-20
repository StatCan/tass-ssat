from enum import Enum
from ..log.logging import getLogger
from .browser import wrapper

log = getLogger(__name__)

def new_driver(uuid, browser_name, configs):
    log.info("Creating driver for: %s", browser_name)
    try:
        wrapper = SupportedDrivers[browser_name.upper()].value
    except KeyError:
        log.warning("%s browser not supported.", browser_name)
        return None

    return wrapper(uuid, configs)


class SupportedDrivers(Enum):
    # Desktop browser drivers
    CHROME = wrapper.ChromeDriverWrapper
    FIREFOX = wrapper.FirefoxDriverWrapper
    EDGE = wrapper.EdgeDriverWrapper
    SAFARI = wrapper.SafariDriverWrapper
