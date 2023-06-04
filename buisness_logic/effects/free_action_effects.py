from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_effect import BaseEffect


class FreeActionEffect(BaseEffect):
    def __init__(self, free_action: BaseAction) -> None:
        if free_action is None:
            raise ValueError("free action cannot be none")
        self._free_action: BaseAction = free_action
        BaseEffect.__init__(self, False)

    @property
    def action(self) -> BaseAction:
        return self._free_action
