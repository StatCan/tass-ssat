import selenium.webdriver.support.expected_conditions as EC
from tass.actions.selenium import locate
from tass.actions.actions import action as act


def wait_element_clickable(driver, action, locator,
                           time=None, page=None, **kwargs):

    def _wait(driver, time, page, locator):
        mark = tuple(locate(page, locator).values())
        return driver.wait_until(EC.element_to_be_clickable, time=time,
                                 mark=mark)

    print('/*/*/*/*/*/*/*/*/*/*/*/*/*//*/*')
    if (action is None):
        _wait(driver, time, page, locator)
    else:
        act(*action)(driver,
                     find=_wait,
                     time=time,
                     page=page,
                     locator=locator,
                     **kwargs)
    print('*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*')


def wait_element_visible(driver, action, locator,
                         time=None, page=None, **kwargs):

    def _wait(driver, time, page, locator):
        mark = tuple(locate(page, locator).values())
        return driver.wait_until(EC.visibility_of_element_located, time=time,
                                 locator=mark)

    print('/*/*/*/*/*/*/*/*/*/*/*/*/*//*/*')
    if (action is None):
        _wait(driver, time, page, locator)
    else:
        act(*action)(driver,
                     find=_wait,
                     time=time,
                     page=page,
                     locator=locator,
                     **kwargs)
    print('*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*')
