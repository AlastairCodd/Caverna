from typing import List, Iterable, Set, Union

from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint


class ActionChoiceLookup(object):
    def __init__(
            self,
            actions: Union[BaseAction, Iterable[BaseAction]],
            constraints: Iterable[BaseConstraint] = None) -> None:
        if actions is None:
            raise ValueError

        self._actions: List[BaseAction] = [actions] if isinstance(actions, BaseAction) else list(actions)
        self._constraints: Set[BaseConstraint] = {} if constraints is None else set(constraints)

    @property
    def actions(self) -> List[BaseAction]:
        return self._actions

    @property
    def constraints(self) -> Iterable[BaseConstraint]:
        return self._constraints
