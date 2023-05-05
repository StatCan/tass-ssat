from enum import Enum
import tass.actions.core as core
import tass.actions.selenium as selenium


class Actions(Enum):
    CORE = core
    SELENIUM = selenium


def action(name, action):
    return getattr(Actions[name.upper()].value, action)
