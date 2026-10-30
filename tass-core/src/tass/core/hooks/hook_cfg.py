from enum import Enum
from dataclasses import dataclass, field


@dataclass(frozen=True)
class HookConfig():
    # Dataclass is used to enable simple fail fast implementation for bad hook configs.
    uuid: str
    when: HookEvent
    hook: str
    order: int = 0
    namespace: str = "core"
    critical: bool | None = None
    args: dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.when, HookEvent) and isinstance(self.when, str):
            self.when = HookEvent[self.when]

@dataclass(frozen=True)
class EventPolicy():
    reversed: bool
    fail_fast: bool
    unwind: HookEvent | None = None
    

class HookEvent(str, Enum):

    def __new__(cls, value, policy):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.policy = policy
        return obj



    BEFORE_RUN = ("before_run", EventPolicy(False, True))
    AFTER_RUN = ("after_run", EventPolicy(True, False, BEFORE_RUN))
    BEFORE_TEST = ("before_test", EventPolicy(False, True))
    AFTER_TEST = ("after_test", EventPolicy(True, False, BEFORE_TEST))
    ON_FAILURE = ("on_failure", EventPolicy(False, False))
    ON_SUCCESS = ("on_success", EventPolicy(True, False))
    ON_START = ("on_start", EventPolicy(False, True))
    ON_FINISH = ("on_finish", EventPolicy(True, False, ON_START))