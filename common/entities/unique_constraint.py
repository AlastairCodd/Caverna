from typing import List

from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint


class UniqueConstraint(BaseConstraint):
    def __init__(
            self,
            unique_action: BaseAction) -> None:
        self._unique_action: BaseAction = unique_action

    @property
    def unique_action(self) -> BaseAction:
        return self._unique_action

    # TODO: Might require changing BaseConstraint signature
    def passes_condition(self, actions: List[BaseAction]) -> bool:
        pass

    def __eq__(self, other) -> bool:
        result: bool = False
        if isinstance(other, self.__class__):
            result = other.unique_action == self._unique_action
        return result
