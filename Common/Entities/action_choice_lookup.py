from typing import List, Iterable, Set, Union, cast

from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint


class ActionChoiceLookup(object):
    def __init__(
            self,
            actions: Union[BaseAction, Iterable[BaseAction]],
            constraints: Union[BaseConstraint, Iterable[BaseConstraint]] = None) -> None:
        if actions is None:
            raise ValueError

        self._actions: List[BaseAction] = [actions] if isinstance(actions, BaseAction) else list(actions)
        self._constraints: List[BaseConstraint]
        if constraints is None:
            self._constraints = []
        else:
            self._constraints = [constraints] if isinstance(constraints, BaseConstraint) else list(constraints)

    @property
    def actions(self) -> List[BaseAction]:
        return self._actions

    @property
    def constraints(self) -> List[BaseConstraint]:
        return self._constraints

    def __str__(self) -> str:
        constraints_string: str = "" if len(self._constraints) == 0 else f", {self._constraints}"
        return f"ActionChoiceLookup({self._actions}{constraints_string})"

    def __eq__(self, other) -> bool:
        result: bool = isinstance(other, ActionChoiceLookup)

        if result:
            cast_other: ActionChoiceLookup = cast(ActionChoiceLookup, other)
            if self is not other:
                action_counts_equal: bool = len(self._actions) == len(cast_other.actions)
                constraints_counts_equal: bool = len(self._constraints) == len(cast_other.constraints)

                result = action_counts_equal and constraints_counts_equal

                if result:
                    action_sequence_equal: bool = True
                    for action in self._actions:
                        does_other_contain_action: bool = action in cast_other.actions
                        if not does_other_contain_action:
                            action_sequence_equal = False
                            break

                    constraints_sequence_equal: bool = True
                    for constraint in self._constraints:
                        does_other_contain_constraint: bool = constraint in cast_other.constraints
                        if not does_other_contain_constraint:
                            constraints_sequence_equal = False
                            break

                    result = action_sequence_equal and constraints_sequence_equal

        return result
