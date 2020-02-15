from typing import List, Iterable, Tuple, Union

from buisness_logic.services.most_points_permutation_ordering_service import MostPointsPermutationOrderingService
from buisness_logic.services.most_resources_permutation_ordering_service import MostResourcesPermutationOrderingService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from common.forges.list_permutation_forge import ListPermutationForge
from common.prototypes.player_prototype import PlayerPrototype
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_action_ordering_service import ActionOrderingService
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_permutation_ordering_service import BasePermutationOrderingService


class ExhaustiveActionOrderingService(ActionOrderingService):
    def __init__(self, permutation_ordering_services: Union[None, List[BasePermutationOrderingService], BasePermutationOrderingService] = None):
        self._player_prototype: PlayerPrototype = PlayerPrototype()
        self._permutation_forge: ListPermutationForge = ListPermutationForge()

        self._permutation_ordering_services: List[BasePermutationOrderingService]
        if permutation_ordering_services is None:
            self._permutation_ordering_services = [MostPointsPermutationOrderingService(), MostResourcesPermutationOrderingService()]
        else:
            if isinstance(permutation_ordering_services, list):
                self._permutation_ordering_services = list(permutation_ordering_services)
            else:
                self._permutation_ordering_services = [permutation_ordering_services]

    def calculated_best_order(
            self,
            actions: ActionChoiceLookup,
            player: Player,
            current_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[List[BaseAction]]:
        if actions is None:
            raise ValueError
        if player is None:
            raise ValueError
        if current_card is None:
            raise ValueError
        if current_dwarf is None:
            raise ValueError

        successful_permutations: List[Tuple[List[BaseAction], int, Player]] = []
        unsuccessful_permutations: List[ResultLookup[int]] = []

        permutation: List[BaseAction]
        permutations: Iterable[List[BaseAction]] = self._permutation_forge.generate_list_partitions(actions.actions)

        for permutation in permutations:
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
                    success_result: Tuple[List[BaseAction], int, Player] = (permutation, successes, player_for_permutation)
                    successful_permutations.append(success_result)
                else:
                    unsuccessful_permutations.append(permutation_result)

        result: Union[ResultLookup[List[BaseAction]], None] = None
        permutation_ordering_service_index: int = 0
        permutation_ordering_service: BasePermutationOrderingService
        ranked_results: List[Tuple[List[BaseAction], int, Player]] = successful_permutations

        if any(ranked_results):
            while result is None:
                if permutation_ordering_service_index >= len(self._permutation_ordering_services):
                    permutation_ordering_service = self._permutation_ordering_services[permutation_ordering_service_index]
                    ordering_result = permutation_ordering_service.find_best_permutation(ranked_results)

                    if ordering_result.flag:
                        result = ResultLookup(True, ordering_result.value[0][0])
                    elif any(ordering_result.value):
                        permutation_ordering_service_index += 1
                        ranked_results = ordering_result.value
                    else:
                        result = ResultLookup(errors=ordering_result.errors)
                else:
                    # if we've exhausted all ordering services, just pick a permutation at random
                    result = ResultLookup(True, ranked_results[0][0])
        else:
            result = ResultLookup(errors="There is not a permutation which allows for all actions to be performed")
        return result
