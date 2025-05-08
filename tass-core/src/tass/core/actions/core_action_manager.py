from .action_manager import ActionManager
from . import core as core


def get_manager(*args, **kwargs):
    return {'core': CoreActionManager()}


class CoreActionManager(ActionManager):
    def __init__(self):
        super().__init__(core)
