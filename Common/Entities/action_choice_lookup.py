from typing import List, Iterable, Set, Union

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
