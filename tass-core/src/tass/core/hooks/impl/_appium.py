from tass.core.log.logging import getLogger
from tass.core.registry import BrokerRegistry
from ..hook_cfg import HookEvent
from tass.core.context import ctx

logger = getLogger(__name__)


def _screenshot(trigger: HookEvent):
    # Get the registered selenium screenshot function.
    screenshot = BrokerRegistry.resolve("appium", "screenshot")
    # Set the name of the screenshot to the test name and triggering event
    name = f"{ctx.test_name}_{trigger}"
    # Take a screenshot via selenium driver
    screenshot(name=name)