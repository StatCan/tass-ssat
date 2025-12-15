import importlib
from enum import Enum
from ..log.logging import getLogger
from .browser import wrapper

log = getLogger(__name__)

def new_driver(uuid, driver_name, **kwargs):
    log.info("Creating driver for: %s", driver_name)
    try:
        wrapper = SupportedDrivers[driver_name.upper()].value
    except KeyError:
        log.warning("%s browser not supported.", driver_name)
        return None

    return wrapper(uuid, **kwargs)


class SupportedDrivers(Enum):
    # Desktop browser drivers
    CHROME = wrapper.ChromeDriverWrapper
    FIREFOX = wrapper.FirefoxDriverWrapper
    EDGE = wrapper.EdgeDriverWrapper
    SAFARI = wrapper.SafariDriverWrapper
    # Mobile drivers
    if importlib.util.find_spec("appium"):
        from .mobile import wrapper as mobile_wrapper
        ANDROID = mobile_wrapper.AndroidDriverWrapper
        IOS = mobile_wrapper.IOSDriverWrapper
