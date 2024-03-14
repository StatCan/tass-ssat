from .action_manager import ActionManager
from . import core as core


class CoreActionManager(ActionManager):
    def __init__(self):
        super().__init__(core)
