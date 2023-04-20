from functools import cache
import math
from typing import TypeVar, List, Generator

T = TypeVar("T")


class ListPermutationForge(object):
    def generate_list_permutations(
            self,
            list_to_permute: List[T]) -> Generator[List[T], None, None]:
        if list_to_permute is None:
            raise ValueError
        number_of_permutations: int = math.factorial(len(list_to_permute))
        for i in range(number_of_permutations):
            yield self.generate_list_permutation_for_index(list_to_permute, i)

    def generate_list_permutation_for_index(
            self,
            list_to_permute: List[T],
            index: int) -> List[T]:
        if list_to_permute is None:
            raise ValueError
        if index < 0:
            raise IndexError
        number_of_items_to_permute = len(list_to_permute)

        if number_of_items_to_permute == 0:
            if index == 0:
                return []
            else:
                raise IndexError("Cannot have non-zero index when given list is empty")

        if number_of_items_to_permute == 1:
            if index == 0:
                return list_to_permute
            else:
                raise IndexError("Cannot have non-zero index when given list is contains only one element")

        taken_index: int
        remaining_index: int
        taken_index, remaining_index = self._get_indicies(index, number_of_items_to_permute)

        result: List[T] = [list_to_permute[taken_index]]

        remaining_list: List[T] = list_to_permute[:taken_index] + list_to_permute[taken_index+1:]
        permuted_remaining_list: List[T] = self.generate_list_permutation_for_index(remaining_list, remaining_index)

        result += permuted_remaining_list
        return result

    @cache
    def _get_indicies(self, index: int, number_of_items_to_permute: int) -> tuple[int, int]:
        number_of_items_to_permute_excluding_first_factorial = math.factorial(number_of_items_to_permute - 1)

        return divmod(index, number_of_items_to_permute_excluding_first_factorial)
