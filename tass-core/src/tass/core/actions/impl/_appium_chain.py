from ...log.logging import getLogger
from . import _selenium_chain as sc


#  For additional documentation, see selenium docs:
#  https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html


logger = getLogger(__name__)


def _perform(driver, **kwargs):
    """Perform all collected actions.

    Execute all selenium Action Chain actions
    that are currenty queued.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.
    """
    sc._perform(driver, **kwargs)


def _reset(driver, **kwargs):
    """Reset stored actions in the Action Chain

    Remove all actions that are currently queued. Action Chain
    will be ready to create new queue.

    Args:
        driver:
            The RemoteWebDriver object that is connected
            to the open browser.

    """
    sc._reset(driver, **kwargs)


def _click(driver,
          find,
          locator,          
          **kwargs):
    sc._click(driver, find, locator, **kwargs)



def _write(driver,
          find,
          locator,
          text,
          **kwargs):
    
    sc._write(driver, find, locator,
                   text=text, **kwargs)


def _move_mouse(driver,
                find, locator,
                xoffset,
                yoffset,
                **kwargs):

    sc._move_mouse(driver, find, locator,
                        xoffset,
                        yoffset,
                        **kwargs)


def _drag_and_drop(driver, *, find, locator, target, xoffset, yoffset, **kwargs):

    sc._drag_and_drop(driver, find, locator, target,
                           xoffset,
                           yoffset,
                           **kwargs)


def _scroll(driver, *, find, locator, deltax, deltay,
           xoffset, yoffset,
           **kwargs):

    sc._scroll(driver, find, locator,
                    deltax, deltay,
                    xoffset, yoffset,
                    **kwargs)
