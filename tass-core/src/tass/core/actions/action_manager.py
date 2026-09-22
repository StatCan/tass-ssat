from tass.core.log.logging import getLogger
from .pool import ExecutorPool
from..registry import CommandBrokers



log = getLogger(__name__)

execpool = ExecutorPool()


class ActionExecutor():
    def action(self, namespace, command, *args, **kwargs):
        raise NotImplementedError('action function not implemented')

    def quit(self):
        # Method called at the end of every case
        # include any cleanup/resetting required
        # to make each case encapsulated.
        raise NotImplementedError('quit function not implemented')


class ActionManager():
    def __init__(self):
        self._executors = {}

    def get(self, alias: str):
        # TODO: catch key errors
        return self._executors[alias]

    def action(self, namespace, command, *args, **kwargs):
        if namespace in self._executors:
            self._executors[namespace].action(namespace, command, *args, **kwargs)
        else:
            CommandBrokers.resolve(namespace, command)(*args, **kwargs)

    def toJson(self):
        return {
            "type": self.__class__.__name__,
            "module": self._module.__name__
            }

    def quit(self):
        for executor in self._executors.values():
            executor.quit()

    @classmethod
    def register_all(cls, managers) -> ActionManager:
        m = cls()
        for manager in managers:
            m._executors.update(execpool.get(**manager))
        return m
