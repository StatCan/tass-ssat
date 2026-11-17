from tass.core.log.logging import getLogger
from tass.core.registry import CommandRegistry
from ..hook_cfg import HookEvent
from tass.core.context import ctx

logger = getLogger(__name__)


def _screenshot(trigger: HookEvent, name: str = None, *args, **kwargs):
    # Get the registered selenium screenshot function.
    screenshot = CommandRegistry.resolve("selenium", "screenshot")
    # Set the name of the screenshot to the test name and triggering event
    _name = name or f"{ctx.test_name.value}_{trigger.value}"
    # Take a screenshot via selenium driver
    driver = ctx.driver("selenium").value()
    driver() # Start the driver if it is not started yet
    screenshot(driver=driver, name=_name)