from typing import List, Dict, Iterable, Callable, Union
from buisness_logic.effects.action_effects import ChangeDecisionVerb
from core.baseClasses.base_action import BaseAction
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ActionCombinationEnum
from common.entities.multiconditional import Conditional


def _combine_and_then(left: Iterable[List[BaseAction]], right: Iterable[List[BaseAction]]) \
        -> List[List[BaseAction]]:
    """Combine the left and right lists in an and then way. (left or right)
    a AND_THEN b = [ab]

    params:
        left: an enumerable of base actions. This cannot be null.
        right: an enumerable of base actions. This cannot be null.

    returns:
        a list containing the possible combined actions. This will never be null."""
    if left is None:
        raise ValueError("left")
    if right is None:
        raise ValueError("right")

    result: List[List[BaseAction]] = []

    for l in left:
        for r in right:
            result.append(l + r)

    return result


def _combine_or(left: Iterable[List[BaseAction]], right: Iterable[List[BaseAction]]) \
        -> List[List[BaseAction]]:
    """Combine the left and right lists in an and then way. (left or right)
    a OR b = [a, b]

    params:
        left: an enumerable of base actions. This cannot be null.
        right: an enumerable of base actions. This cannot be null.

    returns:
        a list containing the possible combined actions. This will never be null."""
    if left is None:
        raise ValueError("left")
    if right is None:
        raise ValueError("right")

    result: List[List[BaseAction]] = []

    for l in left:
        result.append(l)

    for r in right:
        result.append(r)

    return result


def _combine_and_then_or(left: Iterable[List[BaseAction]], right: Iterable[List[BaseAction]]) \
        -> List[List[BaseAction]]:
    """Combine the left and right lists in an and then way. (left or right)
    a AND_THEN_OR b = [ab, b]

    params:
        left: an enumerable of base actions. This cannot be null.
        right: an enumerable of base actions. This cannot be null.

    returns:
        a list containing the possible combined actions. This will never be null."""
    if left is None:
        raise ValueError("left")
    if right is None:
        raise ValueError("right")

    result: List[List[BaseAction]] = []

    for l in left:
        for r in right:
            result.append(l + r)

    for r in right:
        result.append(r)

    return result


def _combine_and_or(left: Iterable[List[BaseAction]], right: Iterable[List[BaseAction]]) \
        -> List[List[BaseAction]]:
    """Combine the left and right lists in an and way. (left or right or left and right)
    a AND_OR b = [a, b, ab]

    params:
        left: an enumerable of base actions. This cannot be null.
        right: an enumerable of base actions. This cannot be null.

    returns:
        a list containing the possible combined actions. This will never be null."""
    if left is None:
        raise ValueError("left")
    if right is None:
        raise ValueError("right")

    result: List[List[BaseAction]] = []

    for l in left:
        result.append(l)

    for r in right:
        result.append(r)

    for l in left:
        for r in right:
            result.append(l + r)

    return result


def _combine_either_or(left: Iterable[List[BaseAction]], right: Iterable[List[BaseAction]]) \
        -> List[List[BaseAction]]:
    """Combine the left and right lists in an either or way. (left or right)
    a EITHER_OR b = [a,b]

    params:
        left: an enumerable of base actions. This cannot be null.
        right: an enumerable of base actions. This cannot be null.

    returns:
        a list containing the possible combined actions. This will never be null."""
    if left is None:
        raise ValueError("left")
    if right is None:
        raise ValueError("right")

    result: List[List[BaseAction]] = []

    for l in left:
        result.append(l)

    for r in right:
        result.append(r)

    return result


class ConditionalService(object):

    def __init__(self):
        """Ctor. Sets up action dictionary for conditional"""
        self._actionDictionary: Dict[
            ActionCombinationEnum,
            Callable[
                [List[List[BaseAction]], List[List[BaseAction]]],
                List[List[BaseAction]]]] = {
            ActionCombinationEnum.EitherOr: _combine_either_or,
            ActionCombinationEnum.AndOr: _combine_and_or,
            ActionCombinationEnum.AndThenOr: _combine_and_then_or,
            ActionCombinationEnum.Or: _combine_or,
            ActionCombinationEnum.AndThen: _combine_and_then}

    def get_possible_choices(
            self,
            conditional: Union[Conditional, BaseAction],
            tile_container: TileContainer = None) -> List[List[BaseAction]]:
        """recurse through the conditional tree in order to find which possible action choices the agent may make

        params:
            conditional. Either a conditional object or an action. This cannot be null
            player (optional):

        returns:
            a list containing all possible (base) actions which can be take. This will never be null."""
        if conditional is None:
            raise ValueError("conditional")
        if isinstance(conditional, BaseAction):
            return [[conditional]]
        if not isinstance(conditional, Conditional):
            raise ValueError("input must be either multiconditional.Conditional or baseAction.BaseAction")

        left: List[List[BaseAction]] = self.get_possible_choices(conditional.get_left_branch(), tile_container)
        right: List[List[BaseAction]] = self.get_possible_choices(conditional.get_right_branch(), tile_container)

        combination_type = conditional.get_combination_type()
        if tile_container is not None:
            change_decision_effects: Iterable[ChangeDecisionVerb] = \
                tile_container.get_effects_of_type(ChangeDecisionVerb)
            for change_decision_effect in change_decision_effects:
                combination_type = change_decision_effect.invoke(combination_type)

        choices: List[List[BaseAction]] = self._actionDictionary[combination_type](left, right)
        return choices