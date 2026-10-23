from tass.core.log.logging import getLogger
from .impl import _selenium as selhooks
from tass.core.registry.hooks import HookEvent
from tass.core.registry import SeleniumHookBroker as Hooks


logger = getLogger(__name__)


@Hooks.hook(events=[HookEvent.ON_SUCCESS,
                    HookEvent.ON_FAILURE,
                    HookEvent.ON_START,
                    HookEvent.ON_FINISH])
def screenshot(trigger: HookEvent, *args, **kwargs):
    selhooks._screenshot(trigger=trigger)