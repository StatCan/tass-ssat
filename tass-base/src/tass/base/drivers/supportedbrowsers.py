from enum import Enum
from ..drivers.browserdriver import (
    ChromeDriver,
    EdgeDriver,
    FirefoxDriver
)


class Browsers(Enum):
    CHROME = ChromeDriver
    FIREFOX = FirefoxDriver
    EDGE = EdgeDriver


def browser(name):
    return Browsers[name.upper()].value
