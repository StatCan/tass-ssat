from tass.core.log.logging import getLogger
from .impl import _appium as apphooks
from tass.core.hooks.hook_cfg import HookEvent
from tass.core.registry import AppiumBroker as Hooks


logger = getLogger(__name__)


@Hooks.hook(events=[HookEvent.ON_FINISH,
                    HookEvent.ON_FAILURE,
                    HookEvent.ON_SUCCESS,
                    HookEvent.ON_START])
def screenshot(trigger: HookEvent, *args, **kwargs):
    apphooks._screenshot(trigger=trigger)