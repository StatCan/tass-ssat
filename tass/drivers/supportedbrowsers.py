from enum import Enum
from tass.drivers.browserdriver import ChromeDriver
from tass.drivers.browserdriver import FirefoxDriver
from tass.drivers.browserdriver import EdgeDriver


class Browsers(Enum):
    CHROME = ChromeDriver
    FIREFOX = FirefoxDriver
    EDGE = EdgeDriver

    def browser(name):
        return Browsers[name.upper()].value
