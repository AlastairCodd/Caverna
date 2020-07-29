from typing import List, Tuple

from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from common.services.point_calculation_service import PointCalculationService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_permutation_ordering_service import BasePermutationOrderingService


class MostPointsPermutationOrderingService(BasePermutationOrderingService):
    def __init__(self):
        self._point_scoring_service: PointCalculationService = PointCalculationService()
        self._min_score: int = 0

    def find_best_permutation(
            self,
            successful_permutations: List[Tuple[List[BaseAction], int, BasePlayerRepository]]) \
            -> ResultLookup[List[Tuple[List[BaseAction], int, BasePlayerRepository]]]:
        if successful_permutations is None:
            raise ValueError
        if len(successful_permutations) == 0:
            raise IndexError(f"{str(successful_permutations)} cannot be empty.")

        permutation: List[BaseAction]
        successes: int
        player: BasePlayerRepository

        best_permutations: List[Tuple[List[BaseAction], int, BasePlayerRepository]] = []
        current_max_points: int = self._min_score
        for (permutation, successes, player) in successful_permutations:
            current_points = self._point_scoring_service.calculate_points(player)
            if current_points > current_max_points:
                best_permutations.clear()
                best_permutations.append((permutation, successes, player))
                current_max_points = current_points
            elif current_points == current_max_points:
                best_permutations.append((permutation, successes, player))

        result: ResultLookup[List[Tuple[List[BaseAction], int, BasePlayerRepository]]]
        if len(best_permutations) == 1:
            result = ResultLookup(True, best_permutations)
        elif len(best_permutations) == 0:
            result = ResultLookup(errors=f"No permutations with score greater than {self._min_score}")
        else:
            result = ResultLookup(False, best_permutations, f"{len(best_permutations)} permutations exist with the same score {current_max_points}")

        return result
