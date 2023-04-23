from typing import List

from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint


class PrecedesConstraint(BaseConstraint):
    def __init__(self, action_one: BaseAction, action_two: BaseAction) -> None:
        if action_one is None:
            raise ValueError
        if action_two is None:
            raise ValueError

        self._action_one: BaseAction = action_one
        self._action_two: BaseAction = action_two

    def passes_condition(self, actions: List[BaseAction]) -> bool:
        return self.get_index_of_first_action_which_fails_constraint(actions) != -1

    def get_index_of_first_action_which_fails_constraint(self, actions: List[BaseAction]) -> int:
        if actions is None:
            raise ValueError

        action_one_location: int = -1
        action_two_location: int = -1
        i: int = 0

        action: BaseAction
        for action in actions:
            if action == self._action_one:
                action_one_location = i
            if action == self._action_two:
                action_two_location = i
            i += 1
            if action_one_location != -1 and action_two_location != -1:
                break

        if action_one_location == -1 or action_two_location == -1:
            return -1

        if action_one_location < action_two_location:
            return -1
        return action_two_location

    def __eq__(self, other) -> bool:
        if isinstance(other, PrecedesConstraint):
            action_one_equal: bool = other._action_one == self._action_one
            action_two_equal: bool = other._action_two == self._action_two
            result: bool = action_one_equal and action_two_equal
            return result
        else:
            return False

    def __repr__(self) -> str:
        return f"PrecedesConstraint({self._action_one!r}, {self._action_two!r})"
