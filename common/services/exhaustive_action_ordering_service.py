from typing import List, Dict, Iterable, Tuple

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from common.prototypes.player_prototype import PlayerPrototype
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_action_ordering_service import ActionOrderingService
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum


class ExhaustiveActionOrderingService(ActionOrderingService):
    def __init__(self):
        self._player_prototype: PlayerPrototype = PlayerPrototype()

    def calculated_best_order(
            self,
            actions: ActionChoiceLookup,
            player: Player,
            current_card: BaseCard,
            current_dwarf: Dwarf) -> List[BaseAction]:
        if actions is None:
            raise ValueError
        if player is None:
            raise ValueError
        if current_card is None:
            raise ValueError
        if current_dwarf is None:
            raise ValueError

        successful_permutations: List[Tuple[int, ResourceContainer]] =[]
        unsuccessful_permutations: List[ResultLookup[int]] = []

        for permutation in self._get_permutations(actions.actions):
            if all(constraint.passes_condition(permutation) for constraint in actions.constraints):
                player_for_permutation: Player = self._player_prototype.clone(player)

                success: bool = True
                successes: int = 0
                errors_for_permutation: List[str] = []

                action: BaseAction
                for action in permutation:
                    action_result: ResultLookup[int] = action.invoke(player_for_permutation, current_card, current_dwarf)

                    if action_result.flag:
                        successes += action_result.value
                    else:
                        success = False

                        error: str
                        for error in action_result.errors:
                            errors_for_permutation.append(error)
                        break

                permutation_result: ResultLookup[int] = ResultLookup(success, successes, errors_for_permutation)
                if success:
                    success_result: Tuple[int, ResourceContainer] = (successes, player_for_permutation)
                    successful_permutations.append(success_result)
                else:
                    unsuccessful_permutations.append(permutation_result)

        if any(successful_permutations):
            pass

        score: Dict[List[BaseAction], Dict[ResourceTypeEnum, int]] = {}
        raise NotImplementedError