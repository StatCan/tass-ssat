from enum import Enum
import tass.actions.core as core
import tass.actions.selenium as selenium


class Actions(Enum):
    CORE = core
    SELENIUM = selenium


def action(name, action):
    """Get the appropriate Actions class

    Args:
        name:
            The string name of the class the action belongs to.
        action:
            The string name of the action to be performed.

    Returns:
        The function belonging to the specified class
        as determined by the action parameter.
    """
    return getattr(Actions[name.upper()].value, action)
