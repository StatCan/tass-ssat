from tass.core.log.logging import getLogger
from .impl import _selenium as selhooks
from tass.core.registry.hooks import HookEvent
from tass.core.registry import SeleniumHookBroker as Hooks


logger = getLogger(__name__)


@Hooks.hook(events=[HookEvent.ON_COMPLETION,
                    HookEvent.ON_FAILURE,
                    HookEvent.ON_START])
def screenshot(trigger: HookEvent, *args, **kwargs):
    selhooks._screenshot(trigger=trigger)