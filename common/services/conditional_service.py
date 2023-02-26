from typing import List, Dict, Iterable, Callable, Union, Optional
from buisness_logic.effects.action_effects import ChangeDecisionVerb
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.precedes_constraint import PrecedesConstraint
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint
from core.enums.caverna_enums import ActionCombinationEnum
from common.entities.multiconditional import Conditional


class ConditionalService(object):

    def __init__(self):
        """Ctor. Sets up action dictionary for conditional"""
        self._action_dictionary: Dict[
            ActionCombinationEnum,
            Callable[
                [List[ActionChoiceLookup], List[ActionChoiceLookup]],
                List[ActionChoiceLookup]]] = {
            ActionCombinationEnum.EitherOr: self._combine_either_or,
            ActionCombinationEnum.AndOr: self._combine_and_or,
            ActionCombinationEnum.And: self._combine_and,
            ActionCombinationEnum.AndThenOr: self._combine_and_then_or,
            ActionCombinationEnum.OrAndThen: self._combine_or_and_then,
            ActionCombinationEnum.Or: self._combine_or,
            ActionCombinationEnum.AndThen: self._combine_and_then}

    def get_possible_choices(
            self,
            conditional: Union[Conditional, BaseAction],
            change_decision_effects: Optional[Iterable[ChangeDecisionVerb]] = None) -> List[ActionChoiceLookup]:
        """recurse through the conditional tree in order to find which possible action choices the agent may make

        :param conditional: Either a conditional object or an action. This cannot be null.
        :param change_decision_effects: (Optional) The effects which change which action choices may be made.

        :returns: A list containing all possible action choice lookups which may be chosen. This will never be null or empty."""
        if conditional is None:
            raise ValueError("Conditional cannot be None")
        if isinstance(conditional, BaseAction):
            return [ActionChoiceLookup(conditional)]
        if not isinstance(conditional, Conditional):
            raise ValueError("input must be either multiconditional.Conditional or baseAction.BaseAction")

        left: List[ActionChoiceLookup] = self.get_possible_choices(conditional.get_left_branch(), change_decision_effects)
        right: List[ActionChoiceLookup] = self.get_possible_choices(conditional.get_right_branch(), change_decision_effects)

        combination_type: ActionCombinationEnum = conditional.get_combination_type()
        if change_decision_effects is not None:
            for change_decision_effect in change_decision_effects:
                combination_type = change_decision_effect.invoke(combination_type)

        choices: List[ActionChoiceLookup] = self._action_dictionary[combination_type](left, right)
        return choices

    def _combine_and_then(
            self,
            left: Iterable[ActionChoiceLookup],
            right: Iterable[ActionChoiceLookup]) -> List[ActionChoiceLookup]:
        """Combine the left and right lists in an and then way. (left or right)
        a AND_THEN b = [ab]

        :param left: an enumerable of base actions. This cannot be null.
        :param right: an enumerable of base actions. This cannot be null.

        :returns: A list containing the possible combined actions. This will never be null."""
        if left is None:
            raise ValueError("left")
        if right is None:
            raise ValueError("right")

        result: List[ActionChoiceLookup] = []

        for l in left:
            for r in right:
                result_actions: List[BaseAction] = l.actions + r.actions
                result_constraints: List[BaseConstraint] = []

                for l_action in l.actions:
                    for r_action in r.actions:
                        result_constraint: BaseConstraint = PrecedesConstraint(l_action, r_action)
                        result_constraints.append(result_constraint)

                if any(l.constraints):
                    result_constraints += l.constraints
                if any(r.constraints):
                    result_constraints += r.constraints

                result_lookup: ActionChoiceLookup = ActionChoiceLookup(result_actions, result_constraints)
                if result_lookup not in result:
                    result.append(result_lookup)

        return result

    def _combine_or(self, left: Iterable[ActionChoiceLookup], right: Iterable[ActionChoiceLookup]) \
            -> List[ActionChoiceLookup]:
        """Combine the left and right lists in an and then way. (left or right)
        a OR b = [a, b]

        :param left: an enumerable of base actions. This cannot be null.
        :param right: an enumerable of base actions. This cannot be null.

        :returns: A list containing the possible combined actions. This will never be null."""
        if left is None:
            raise ValueError("left")
        if right is None:
            raise ValueError("right")

        result: List[ActionChoiceLookup] = []

        for l in left:
            result.append(l)

        for r in right:
            result.append(r)

        return result

    def _combine_and_then_or(self, left: Iterable[ActionChoiceLookup], right: Iterable[ActionChoiceLookup]) \
            -> List[ActionChoiceLookup]:
        """Combine the left and right lists in an and then way. (left or right)
        a AND_THEN_OR b = [ab, b]

        :param left: an enumerable of base actions. This cannot be null.
        :param right: an enumerable of base actions. This cannot be null.

        :returns: A list containing the possible combined actions. This will never be null."""
        if left is None:
            raise ValueError("left")
        if right is None:
            raise ValueError("right")

        result: List[ActionChoiceLookup] = self._combine_and_then(left, right)

        for r in right:
            if r not in result:
                result.append(r)

        return result

    def _combine_and_or(self, left: Iterable[ActionChoiceLookup], right: Iterable[ActionChoiceLookup]) \
            -> List[ActionChoiceLookup]:
        """Combine the left and right lists in an and way. (left or right or left and right)
        a AND_OR b = [a, b, ab, ba]

        :param left: an enumerable of base actions. This cannot be null.
        :param right: an enumerable of base actions. This cannot be null.

        :returns: A list containing the possible combined actions. This will never be null."""
        if left is None:
            raise ValueError("left")
        if right is None:
            raise ValueError("right")

        result: List[ActionChoiceLookup] = []

        for l in left:
            result.append(l)

        for r in right:
            result.append(r)

        for l in left:
            for r in right:
                result_actions: List[BaseAction] = l.actions + r.actions
                result_constraints: List[BaseConstraint] = list(l.constraints) + list(r.constraints)

                result_lookup: ActionChoiceLookup = ActionChoiceLookup(result_actions, result_constraints)
                result.append(result_lookup)

        return result

    def _combine_and(
            self,
            left: Iterable[ActionChoiceLookup],
            right: Iterable[ActionChoiceLookup]) -> List[ActionChoiceLookup]:
        """Combine the left and right lists in an and way. (left or right or left and right)
        a AND_OR b = [ab, ba]

        :param left: an enumerable of base actions. This cannot be null.
        :param right: an enumerable of base actions. This cannot be null.

        :returns: A list containing the possible combined actions. This will never be null."""
        if left is None:
            raise ValueError("left")
        if right is None:
            raise ValueError("right")

        result: List[ActionChoiceLookup] = []

        for l in left:
            for r in right:
                result_actions: List[BaseAction] = l.actions + r.actions
                result_constraints: List[BaseConstraint] = list(l.constraints) + list(r.constraints)

                result_lookup: ActionChoiceLookup = ActionChoiceLookup(result_actions, result_constraints)
                result.append(result_lookup)

        return result

    def _combine_or_and_then(
            self,
            left: Iterable[ActionChoiceLookup],
            right: Iterable[ActionChoiceLookup]) -> List[ActionChoiceLookup]:
        """Combine the left and right lists in an and then way. (left or right)
        a OR_AND_THEN b = [a, ab]

        :param left: an enumerable of base actions. This cannot be null.
        :param right: an enumerable of base actions. This cannot be null.

        :returns: A list containing the possible combined actions. This will never be null."""
        if left is None:
            raise ValueError("left")
        if right is None:
            raise ValueError("right")

        result: List[ActionChoiceLookup] = self._combine_and_then(left, right)

        for l in left:
            result.append(l)

        return result

    def _combine_either_or(self, left: Iterable[ActionChoiceLookup], right: Iterable[ActionChoiceLookup]) \
            -> List[ActionChoiceLookup]:
        """Combine the left and right action choice lookups in an "either or" way. (left or right)
        a EITHER_OR b = [a,b]

        :param left: an enumerable of base actions. This cannot be null.
        :param right: an enumerable of base actions. This cannot be null.

        :returns: A list containing the possible combined actions. This will never be null."""
        if left is None:
            raise ValueError("left")
        if right is None:
            raise ValueError("right")

        result: List[ActionChoiceLookup] = []

        for l in left:
            result.append(l)

        for r in right:
            result.append(r)

        return result
