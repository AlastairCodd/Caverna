from functools import cache
import math
from typing import TypeVar, List, Generator

T = TypeVar("T")


class PruningListPermutationForge(object):
    def __init__(self):
        self._index: int = -1
        self._number_of_items_to_permute: int = -1

    def generate_list_permutations(
            self,
            list_to_permute: List[T]) -> Generator[List[T], None, None]:
        if list_to_permute is None:
            raise ValueError
        self._number_of_items_to_permute: int = len(list_to_permute)
        number_of_permutations: int = math.factorial(self._number_of_items_to_permute)
        # this will be immediately incremented on entering the loop
        self._index = -1

        while self._index < number_of_permutations:
            self._index += 1
            yield self.generate_list_permutation_for_index(list_to_permute, self._index, self._number_of_items_to_permute)

    def generate_list_permutation_for_index(
            self,
            list_to_permute: List[T],
            index: int,
            number_of_items_to_permute: int) -> List[T]:
        if list_to_permute is None:
            raise ValueError
        if index < 0:
            raise IndexError
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
        permuted_remaining_list: List[T] = self.generate_list_permutation_for_index(remaining_list, remaining_index, number_of_items_to_permute - 1)

        result += permuted_remaining_list
        return result

    def mark_last_permutation_as_invalid(
            self,
            first_invalid_item_in_permutation: int) -> None:
        # given the assumption that the `first_invalid_item_in_permutation` will
        #   occur at the first index possible (ie, first time that we end up with
        #   --a--b (a<b)), then we only need to count until a is no longer in the
        #   same position. this is equivalent to incrementing by ...UNKNOWN.
        # this assumption only holds for precedes constraints, i think?
        increment_by = math.factorial(self._number_of_items_to_permute - first_invalid_item_in_permutation - 1)
        #print(f"incrementing by {increment_by}=({self._number_of_items_to_permute} - {first_invalid_item_in_permutation} - 1)!")
        self._index += increment_by

        # this service works by counting from 0 to n!, where n is the number of items
        #   for i in n
        #     divmod(

    @cache
    def _get_indicies(self, index: int, number_of_items_to_permute: int) -> tuple[int, int]:
        number_of_items_to_permute_excluding_first_factorial = math.factorial(number_of_items_to_permute - 1)

        return divmod(index, number_of_items_to_permute_excluding_first_factorial)
