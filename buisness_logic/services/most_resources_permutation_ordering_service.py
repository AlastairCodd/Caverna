from typing import List, Tuple

from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_permutation_ordering_service import BasePermutationOrderingService


class MostResourcesPermutationOrderingService(BasePermutationOrderingService):
    def __init__(self):
        self._min_resources: int = 0

    def find_best_permutation(self, successful_permutations: List[Tuple[List[BaseAction], int, BasePlayerRepository]]) \
            -> ResultLookup[List[Tuple[List[BaseAction], int, BasePlayerRepository]]]:
        if successful_permutations is None:
            raise ValueError
        if len(successful_permutations) == 0:
            raise IndexError(f"{str(successful_permutations)} cannot be empty.")

        permutation: List[BaseAction]
        successes: int
        player: BasePlayerRepository

        best_permutations: List[Tuple[List[BaseAction], int, BasePlayerRepository]] = []
        current_max_resources: int = self._min_resources

        for (permutation, successes, player) in successful_permutations:
            current_resources = sum(player.resources.values())
            if current_resources > current_max_resources:
                best_permutations.clear()
                best_permutations.append((permutation, successes, player))
                current_max_resources = current_resources
            elif current_resources == current_max_resources:
                best_permutations.append((permutation, successes, player))

        result: ResultLookup[List[Tuple[List[BaseAction], int, BasePlayerRepository]]]
        if len(best_permutations) == 1:
            result = ResultLookup(True, best_permutations)
        elif len(best_permutations) == 0:
            raise IndexError("DEV ERROR: Should not be able to have any/all permutations with fewer than zero resources.")
        else:
            result = ResultLookup(False, best_permutations, f"{len(best_permutations)} permutations exist with the same quantity of resources {current_max_resources}")

        return result
