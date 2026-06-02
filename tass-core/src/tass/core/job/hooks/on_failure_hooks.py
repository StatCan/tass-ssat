import inspect
import pathlib
from datetime import datetime
from ...log.logging import getLogger


log = getLogger(__name__)


def prerequisite(capability):
    def decorator(func):
        def wrapper(manager, *args, **kwargs):
            _ = manager.driver
            capable = hasattr(_, capability)
            is_function = inspect.ismethod(getattr(_, capability))
            if not capable or not is_function:
                log.warning("%s does not meet the prerequisite: %s", func.__name__, capability)
                return
            else:
                func(manager, *args, **kwargs)
        return wrapper
    return decorator
    


@prerequisite(capability="screenshot")
def tasscase_hook_screenshot_on_failure(manager, test_uuid):
    driver = manager.driver
    screenshotsfldr = pathlib.Path("screenshots").resolve()
    # Sort png by browser config
    screenshotsfldr = screenshotsfldr.joinpath("errors").resolve()
    screenshotsfldr.mkdir(exist_ok=True, parents=True)
    date_tag = datetime.now().strftime("%d-%m-%y--%H-%M-%S")
    name = test_uuid  # Remove spaces from file name
    file_name = "_".join([name, date_tag])
    _file = screenshotsfldr.joinpath(file_name).with_suffix(".png")
    out = str(_file.resolve())
    log.debug("Saving failure screenshot as: %s", out)

    try:
        status = driver().save_screenshot(out)
    except WebDriverException as e:
        log.warning("Something went wrong, %s -- Trying again", e)
        status = driver().save_screenshot(out)

    if status:
        log.debug("Screenshot saved successfully.")
    else:
        log.warning("Screenshot was not saved!")
