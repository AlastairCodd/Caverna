from typing import List, Dict, NamedTuple

from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint
from core.services.base_constraint_validator import BaseConstraintValidator
from common.entities.precedes_constraint import PrecedesConstraint

class CondensedConstraint(NamedTuple):
    must_precede: BaseAction
    actions: List[BaseAction]


class CollatingConstraintValidator(BaseConstraintValidator):
    def __init__(
            self,
            constraints: List[BaseConstraint]) -> None:
        self._constraints: List[CondensedConstraint] = []
        for constraint in constraints:
            if not isinstance(constraint, PrecedesConstraint):
                raise ValueError("Constraint validator only works for precedes constraints")
            self._get_condensed_constraint_to_append_to(constraint).actions.append(constraint._action_two)
        self._logging: bool = False

    def get_index_of_first_action_which_fails_constraints(
            self,
            permutation: List[BaseAction]) -> int:
        actions_with_index: Dict[BaseAction, int] = {action: i for (i, action) in enumerate(permutation)}

        index_of_first_action_that_fails_to_pass_constraint = 100 # arbitrary large number, shouldn't ever have 100 actions
        if self._logging:
            constraint: PrecedesConstraint

        for (must_precede, actions) in self._constraints:
            index_that_must_precede = actions_with_index[must_precede]
            for action in actions:
                index_of_action = actions_with_index[action]
                if index_of_action > index_that_must_precede:
                    continue
                if index_of_first_action_that_fails_to_pass_constraint <= index_of_action:
                    continue
                index_of_first_action_that_fails_to_pass_constraint = index_of_action
                if self._logging:
                    constraint = PrecedesConstraint(must_precede, action)

        if index_of_first_action_that_fails_to_pass_constraint == 100:
            return -1
        if self._logging:
            print(constraint, index_of_first_action_that_fails_to_pass_constraint)
        return index_of_first_action_that_fails_to_pass_constraint

    def _get_condensed_constraint_to_append_to(self, constraint) -> CondensedConstraint:
        for condensed in self._constraints:
            if condensed.must_precede == constraint._action_one:
                return condensed
        new_condensed = CondensedConstraint(constraint._action_one, [])
        self._constraints.append(new_condensed)
        return new_condensed
