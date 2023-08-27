from typing import List, NamedTuple

from line_profiler import profile

from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint
from common.entities.precedes_constraint import PrecedesConstraint


class BitmanipConstraintValidator(object):
    def __init__(
            self,
            constraints: List[BaseConstraint]) -> None:
        self._constraints = {}
        self._number_of_constraints = len(constraints)

        for (i, constraint) in enumerate(constraints):
            if not isinstance(constraint, PrecedesConstraint):
                raise ValueError("Constraint validator only works for precedes constraints")
            #print(f"constraint {i}: {constraint!r}")
            self._constraints.setdefault(constraint._action_one, [])
            self._constraints.setdefault(constraint._action_two, [])

            offset = 1 << i

            self._constraints[constraint._action_one].append((i, True, offset))
            self._constraints[constraint._action_two].append((i, False, offset))

    @profile
    def get_index_of_first_action_which_fails_constraints(
            self,
            permutation: List[BaseAction]) -> int:
        already_considered = 0
        for (i, action) in enumerate(permutation):
            if action not in self._constraints:
                continue
            #print()
            constraints_on_action = self._constraints[action]
            #print(i, "action", repr(action))
            #print("constraints", constraints_on_action)
            for (constraint_index, is_first_action, offset) in constraints_on_action:
                #print(f"{offset=:b}")
                if already_considered & offset != 0:
                    #print(" ", constraint_index, "skipped")
                    continue
                if not is_first_action:
                    #print(constraint_index, "bad", i)
                    return i
                #print(constraint_index, "good")
                already_considered |= offset
            #print(f"{self._already_considered:b}")
        return -1
