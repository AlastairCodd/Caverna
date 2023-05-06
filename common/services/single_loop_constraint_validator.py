from typing import List, Dict, NamedTuple

from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint
from common.entities.precedes_constraint import PrecedesConstraint


class SingleLoopConstraintValidator(object):
    def __init__(
            self,
            constraints: List[BaseConstraint]) -> None:
        self._constraints: Dict[BaseAction, List[BaseConstraint]] = {}
        for constraint in constraints:
            if not isinstance(constraint, PrecedesConstraint):
                raise ValueError("Constraint validator only works for precedes constraints")
            self._constraints.setdefault(constraint._action_one, [])
            self._constraints.setdefault(constraint._action_two, [])
            self._constraints[constraint._action_one].append(constraint)
            self._constraints[constraint._action_two].append(constraint)

    def get_index_of_first_action_which_fails_constraints(
            self,
            permutation: List[BaseAction]) -> int:
        constraints = {action: constraints.copy for action, constraints in self._constraints.items()}
        for (i, action) in enumerate(permutation):
            constraints_on_action = self._constraints[action]
            for constraint in constraints_on_action:
                if constraint._action_two == action:
                    print(constraint, i)
                    return i
                constraints_on_action.remove(constraint)
        return -1
