from dataclasses import dataclass
from typing import Any
from tass.core.log.logging import getLogger
from tass.core.registry import HookRegistry
from tass.core.registry.hooks import HookDefinition
from tass.core.hooks.hook_cfg import HookEvent, HookConfig
from tass.core.exceptions.hook_errors import CriticalHookExecutionError, HookExecutionError


logger = getLogger(__name__)


@dataclass(frozen=True)
class HookResult():
    hook: str
    trigger: HookEvent
    ok: bool
    result: Any = None
    critical: bool = False
    error: Exception | None = None


class HookCleanup():
    def __init__(self, name, func, message=None):
        self._name = name
        self._func = func
        self._msg = message
    

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)
    
    @property
    def name(self):
        return self._name
    
    @property
    def message(self):
        return self._msg


class HookDispatcher():
    def __init__(self):
        self._unwind: dict[HookEvent, list[HookCleanup]] = {}


    def fire(self, trigger: HookEvent, hooks: list[HookConfig], *args, **kwargs):
        try:
            policy = trigger.policy
            actionable = [h for h in hooks if h.when == trigger]
            actionable.sort(key=lambda h: h.order)
            if policy.reversed:
                actionable.reverse()
            results = []
            for config in actionable:
                result = _fire(config)
                results.append(result)
                if result.ok:
                    continue
                elif not result.critical:
                    continue
                elif policy.fail_fast:
                    break
            failures = [r for r in results if not r.ok]
            if any(r.critical for r in failures):
                raise CriticalHookExecutionError("CRITICAL -- %d hook%s failed.",
                                                trigger,
                                                failures,
                                                len(failures),
                                                "s" if len(failures)>1 else "")
            else:
                raise HookExecutionError("%d hook%s failed.",
                                                trigger,
                                                failures,
                                                len(failures),
                                                "s" if len(failures)>1 else "")
        finally:
            if policy.unwind:
                self.unwind(policy.unwind)

    def _push_unwind(self, event):
        if event not in self._unwind:
            logger.debug("Created deferred cleanup queue for %s", event)
            self._unwind[event] = []
        def _push(name, cleanup, *, message=None):
            cleaner = HookCleanup(name, cleanup, message=message)           
            self._unwind[event].append(cleaner)
            logger.debug("Queued cleanup function for: %s", cleaner.name)
        return _push

    def unwind(self, event):
        logger.debug("Cleaning up from %s", event)
        _ = self._unwind.get(event, [])
        while _:
            cleanup = _.pop()
            logger.debug("Cleaning up after: %s", cleanup.name)
            if cleanup.message:
                logger.info(cleanup.message)
            cleanup()
        logger.debug("Finished %s cleanup", event)

    def unwind_all(self):
        if not all(self._unwind.values()):
            return
        logger.warning("Cleanup events were missed.")
        for event, hooks in self._unwind.items():
            logger.debug("Cleaning up from missed %s", event)
            while hooks:
                cleanup = _.pop()
                logger.debug("Cleaning up after: %s", cleanup.name)
                if cleanup.message:
                    logger.info(cleanup.message)
                cleanup()
            logger.debug("Finished missed %s cleanup", event)


def _fire(trigger: HookEvent, hook_cfg: HookConfig):
    try:
        hook = HookRegistry.resolve(hook_cfg.namespace, hook_cfg.hook)
        critical = _is_critical(hook_cfg, hook)
        _name = f"{hook_cfg.namespace}.{hook_cfg.hook}"
        result = hook(hook_cfg.args)
    except Exception as e:
        logger.exception("Hook execution failed.", e)
        return HookResult(_name, trigger, False, result, critical, e)
    logger.debug("Hook: %s completed", _name)
    return HookResult(_name, trigger, True, result, critical)


def _is_critical(hook_cfg: HookConfig, hook: HookDefinition):
    if hook_cfg.critical is not None:
        return hook_cfg.critical
    else:
        return hook.critical