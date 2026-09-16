import pathlib
from datetime import datetime
from . import _selenium as sel
from ...log.logging import getLogger
from selenium.common.exceptions import WebDriverException


logger = getLogger(__name__)


def _click(driver,
           find,
           pointer_type,
           **kwargs):
    # JavaScript used to trigger a click (tap) event on the element
    # Bypasses issues clicking edge case elements that may give wrong
    # coordinates with default click.
    _valid_pointers = ['pen', 'touch', 'mouse']
    _pointer = pointer_type if pointer_type in _valid_pointers else 'touch'
    options = (
        "{'bubbles': true, 'pointerType': '"
        f"{_pointer}"
        "'}"
    )
    script = (
        # Scroll element to center of view
        "arguments[0].scrollIntoView({'block': 'center'});"
        # Fire click event
        f"arguments[0].dispatchEvent(new PointerEvent('click', {options}))"
    )

    ele = find(driver, **kwargs)

    driver().execute_script(script, ele)
    logger.debug("Element clicked")


def _write(driver, find, text, **kwargs):
    sel._write(driver, find, text, **kwargs)


def _write_stored_value(driver,
                        find,
                        text_key,
                        **kwargs):
    sel._write_stored_value(driver, find, text_key, **kwargs)


def _select_dropdown(driver,
                    find,
                    value,
                    using,
                    **kwargs):
    sel._select_dropdown(driver, find, value, using, **kwargs)


def _clear(driver, find, **kwargs):
    sel._clear(driver, find, **kwargs)


def _load_url(driver, url):
    sel._load_url(driver, url)


def _load_file(driver, relative_path):
    sel._load_file(driver, relative_path)


def _load_page(driver, page, url_key, use_local):
    sel._load_page(driver, page, url_key, use_local)


def _read_attribute(driver,
                   find,
                   attribute,
                   **kwargs):
    return sel._read_attribute(driver, find, attribute, **kwargs)


def _read_css(driver, find, attribute, **kwargs):
    return sel._read_css(driver, find, attribute, **kwargs)


def _read_text(driver, find, **kwargs):
    return sel._read_text(driver, find, **kwargs)


def _switch_frame(driver, find, frame, page):
    sel._switch_frame(driver, find, frame, page)


def _switch_window(driver, title, page):
    sel._switch_window(driver, title, page)


def _close(driver):
    sel._close(driver)


def _quit(driver):
    sel._quit(driver)


def _handle_alert(driver, handle, text):
    sel._handle_alert(driver, handle, text)


def _screenshot(driver,
               find,
               name,
               locator,
               **kwargs):

    screenshotsfldr = pathlib.Path("screenshots").resolve()
    # Sort png by browser config
    driverfldr = [driver.os, driver.device_name, driver.platform_version]
    screenshotsfldr = screenshotsfldr.joinpath(*driverfldr).resolve()
    screenshotsfldr.mkdir(exist_ok=True, parents=True)
    date_tag = datetime.now().strftime("%d-%m-%y--%H-%M-%S")
    name = name.replace(" ", "_")  # Remove spaces from file name
    file_name = "_".join([name, date_tag])
    _file = screenshotsfldr.joinpath(file_name).with_suffix(".png")
    count = 0

    while _file.exists():
        count += 1
        file_name = "".join([name, date_tag, f"({count})"])
        _file = _file.with_stem(file_name)

    out = str(_file.resolve())
    logger.info("Saving screenshot as: %s", out)

    if locator:
        status = find(driver, locator, **kwargs).screenshot(out)
    else:
        status = driver().save_screenshot(out)

    if status:
        logger.info("Screenshot saved successfully.")
    else:
        logger.warning("Screenshot was not saved!")

    return out


# / / / / / / / Assertions / / / / / / /
# TODO: If the appium command only calls the selenium command, does it need to be added to the registry?
def _assert_alert_displayed(driver, text, soft):
    sel._assert_alert_displayed(driver, text, soft)


def _assert_page_is_open(driver, find, page,
                        soft, page_id):
    sel._assert_page_is_open(driver, find,
                             page, soft,
                            page_id)


def _assert_contains_text(driver, find, text, 
                         soft, exact, **kwargs):
    sel._assert_contains_text(driver, find, text, 
                             soft, exact, **kwargs)


def _assert_displayed(driver,
                     find,
                     soft,
                     **kwargs):
    sel._assert_displayed(driver, find, soft, **kwargs)


def _assert_not_displayed(driver,
                         find,
                         soft,
                         **kwargs):
    sel._assert_not_displayed(driver, find, soft, **kwargs)


def _assert_attribute_contains_value(driver,
                                     find,
                                     attribute,
                                     value,
                                     soft,
                                     exact,
                                     **kwargs):
    sel._assert_attribute_contains_value(driver, find, attribute,
                                         value, soft,
                                         exact, **kwargs)