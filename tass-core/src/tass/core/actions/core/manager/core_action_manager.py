from ...action_manager import ActionExecutor
from ..registry import module_registry as executor


def get_manager(*args, **kwargs):
    return {'core': CoreActionManager()}


class CoreActionExecutor(ActionExecutor):
    # Executors are only needed when custom configurations are needed.
    def __init__(self):
        super().__init__()

    def action(self, namespace, command, *args, **kwargs):
        executor.resolve(namespace, command)(*args, **kwargs)
