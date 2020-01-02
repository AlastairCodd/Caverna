from abc import ABC, abstractmethod
from typing import Tuple, List

from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction


class BasePermutationOrderingService(ABC):
    @abstractmethod
    def find_best_permutation(self, successful_permutations: List[Tuple[List[BaseAction], int, Player]]) \
            -> ResultLookup[List[Tuple[List[BaseAction], int, Player]]]:
        """Finds the best permutation out of the given successful permutations (successful in that all actions can be performed by a given player)
        :param successful_permutations: A list containing tuples of
            - Ordered Actions (permutations),
            - the number of successful permutations,
            - and the player has after the actions are performed in the given order. This cannot be null.
        :returns: A result lookup containing the 'best' (by some metric) tuples of actions, successes and player end state.
            The flag will be true if a unique best permutation was found, and false (with an error) if more or less than one were found.
            This will never be null."""
        pass
