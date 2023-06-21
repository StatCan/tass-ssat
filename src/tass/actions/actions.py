from enum import Enum


def importSelenium():
    import tass.actions.selenium as selenium
    return selenium


def importSelWait():
    import tass.actions.selenium_wait as selwait
    return selwait


def importCore():
    import tass.actions.core as core
    return core


class Actions(Enum):
    CORE = importCore
    SELENIUM = importSelenium
    SELWAIT = importSelWait

    def __call__(self):
        return self.value()


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
    module = getattr(Actions, name.upper())()
    return getattr(module, action)
