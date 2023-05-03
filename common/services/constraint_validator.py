from typing import List, Dict, NamedTuple

from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint
from common.entities.precedes_constraint import PrecedesConstraint

class CondensedConstraint(NamedTuple):
    must_precede: BaseAction
    actions: List[BaseAction]


class ConstraintValidator(object):
    def __init__(
            self,
            constraints: List[BaseConstraint]) -> None:
        self._constraints: List[CondensedConstraint] = []
        for constraint in constraints:
            if not isinstance(constraint, PrecedesConstraint):
                raise ValueError("Constraint validator only works for precedes constraints")
            self._get_condensed_constraint_to_append_to(constraint).actions.append(constraint._action_two)

    def get_index_of_first_action_which_fails_constraints(
            self,
            permutation: List[BaseAction]) -> int:
        actions_with_index: Dict[BaseAction, int] = {action: i for (i, action) in enumerate(permutation)}

        index_of_first_action_that_fails_to_pass_constraint = 100 # arbitrary large number, shouldn't ever have 100 actions

        for (must_precede, actions) in self._constraints:
            index_of_first_action_that_fails_to_pass_constraint = self._get_first_action_which_fails_to_pass_constraint(must_precede, actions, actions_with_index, index_of_first_action_that_fails_to_pass_constraint)
        return -1 if index_of_first_action_that_fails_to_pass_constraint == 100 else index_of_first_action_that_fails_to_pass_constraint

    def _get_condensed_constraint_to_append_to(self, constraint) -> CondensedConstraint:
        for condensed in self._constraints:
            if condensed.must_precede == constraint._action_one:
                return condensed
        new_condensed = CondensedConstraint(constraint._action_one, [])
        self._constraints.append(new_condensed)
        return new_condensed

    def _get_first_action_which_fails_to_pass_constraint(
            self,
            must_precede,
            actions,
            actions_with_index,
            index_of_first_action_that_fails_to_pass_constraint) -> int:
        index_that_must_precede = self._get_index_of_action(actions_with_index, must_precede)
        for action in actions:
            index_of_action = self._get_index_of_action(actions_with_index, action)
            index_of_first_action_that_fails_to_pass_constraint = self._get_new_index_constraint(index_of_action, index_that_must_precede, index_of_first_action_that_fails_to_pass_constraint)
        return index_of_first_action_that_fails_to_pass_constraint

    def _get_index_of_action(self, actions_with_index, action) -> int:
        return actions_with_index[action]

    # rename me when you're not so tired
    def _get_new_index_constraint(
            self,
            index_of_action,
            index_that_must_precede,
            index_of_first_action_that_fails_to_pass_constraint) -> int:
        # action index shouldn't ever be equal to preceding action index
        if index_of_action > index_that_must_precede:
            return index_of_first_action_that_fails_to_pass_constraint
        if index_of_first_action_that_fails_to_pass_constraint > index_of_action:
            return index_of_action
        return index_of_first_action_that_fails_to_pass_constraint
