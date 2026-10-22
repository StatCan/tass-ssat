from enum import Enum
from dataclasses import dataclass, field


@dataclass(frozen=True)
class HookConfig():
    # Dataclass is used to enable simple fail fast implementation for bad hook configs.
    when: HookEvent
    hook: str
    namespace: str = "core"
    critical: bool = False
    args: dict = field(default_factory=dict)

@dataclass(frozen=True)
class EventPolicy():
    reverse: bool
    fail_fast: bool
    

class HookEvent(str, Enum):

    def __new__(cls, value, policy):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.policy = policy
        return obj



    BEFORE_RUN = ("before_run", EventPolicy(False, True))
    AFTER_RUN = ("after_run", EventPolicy(True, False))
    BEFORE_TEST = ("before_test", EventPolicy(False, True))
    AFTER_TEST = ("after_test", EventPolicy(True, False))
    ON_FAILURE = ("on_failure", EventPolicy(True, False))
    ON_COMPLETION = ("on_completion", EventPolicy(True, False))
    ON_START = ("on_start", EventPolicy(False, True))