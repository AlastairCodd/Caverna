from typing import List, NamedTuple

from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint
from common.entities.precedes_constraint import PrecedesConstraint


class SingleLoopConstraintValidator(object):
    def __init__(
            self,
            constraints: List[BaseConstraint]) -> None:
        self._constraints = {}
        self._number_of_constraints = len(constraints)
        self._already_considered: List[bool] = [False for _ in range(self._number_of_constraints)]

        for (i, constraint) in enumerate(constraints):
            if not isinstance(constraint, PrecedesConstraint):
                raise ValueError("Constraint validator only works for precedes constraints")
            self._constraints.setdefault(constraint._action_one, [])
            self._constraints.setdefault(constraint._action_two, [])

            self._constraints[constraint._action_one].append((i, True))
            self._constraints[constraint._action_two].append((i, False))

    def get_index_of_first_action_which_fails_constraints(
            self,
            permutation: List[BaseAction]) -> int:
        self._reset()
        for (i, action) in enumerate(permutation):
            #print()
            if action not in self._constraints:
                continue
            constraints_on_action = self._constraints[action]
            #print(i, "action", repr(action))
            #print("constraints", constraints_on_action)
            for (constraint_index, is_first_action) in constraints_on_action:
                if self._already_considered[constraint_index]:
                    #print(" ", constraint, "skipped")
                    continue
                if not is_first_action:
                    #print(constraint, i)
                    return i
                #print(constraint, "good")
                self._already_considered[constraint_index] = True
        return -1

    def _reset(self) -> None:
        self._already_considered = [False for _ in range(self._number_of_constraints)]

