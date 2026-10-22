from dataclasses import dataclass
from tass.core.registry import HookRegistry
from tass.core.hooks.hook_cfg import HookEvent, HookConfig


@dataclass(frozen=True)
class HookResult():
    hook: str
    trigger: HookEvent
    ok: bool
    critical: bool = False
    error: Exception | None = None


class HookDispatcher():
    def fire(self, trigger: HookEvent, hooks: list[HookConfig], *args, **kwargs):
        policy = trigger.policy
        actionable = [h for h in hooks if h.when == trigger]
        if policy.reversed:
            actionable.reverse()
        results = []
        for config in actionable:
            result = self._fire(config.namespace, config.hook, **config.args)
            results.append(result)
            if result.ok or not result.critical:
                continue
            if policy.fail_fast:
                break
        failures = [r for r in results if not r.ok]
        if any(r.critical for r in failures):
            # TODO: raise CriticalHookExecutionError
            pass
        else:
            # TODO: raise HookExecutionError
            pass





    def _fire(self, namespace, hook, *args, **kwargs):
        hook = HookRegistry.resolve(namespace, hook)