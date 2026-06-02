from .action_manager import ActionManager
from . import core as core


def get_manager(core_configs=None, *args, **kwargs):
    if not core_configs:
        manager = {
            "driver": None,
            "config": {}
            }
    else:
        manager = {
            "driver": None,
            "config": core_configs
        }
    return {'core': CoreActionManager(manager)}


class CoreActionManager(ActionManager):
    def __init__(self, manager):
        super().__init__(core, manager)
