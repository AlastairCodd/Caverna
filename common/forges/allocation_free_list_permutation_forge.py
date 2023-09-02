import math
from typing import TypeVar, List, Generator
import logging

from line_profiler import profile

from core.forges.base_list_permutation_forge import BaseListPermutationForge
from core.constants.logging import DollarMessage as __

T = TypeVar("T")


class AllocationFreeListPermutationForge(BaseListPermutationForge):
    def __init__(self):
        self._logging: bool = False

        self._index: int = -1
        self._number_of_items_to_permute: int = -1
        self._factorial_cache: Optional[List[int]] = None

    def generate_list_permutations(
            self,
            list_to_permute: List[T]) -> Generator[List[T], None, None]:
        if list_to_permute is None:
            raise ValueError
        self._number_of_items_to_permute: int = len(list_to_permute)
        self._factorial_cache = [math.factorial(i) for i in range(self._number_of_items_to_permute)]

        number_of_permutations: int = self._factorial_cache[-1] * self._number_of_items_to_permute
        logging.debug(__(
            "permuting {i} items, {p} possible permutations",
            i=self._number_of_items_to_permute,
            p=number_of_permutations))
        # this will be immediately incremented on entering the loop
        self._index = -1
        self._result = [0 for _ in self._factorial_cache]

        while self._index < number_of_permutations - 1:
            self._index += 1
            yield self.generate_list_permutation_for_index(list_to_permute, self._index, self._number_of_items_to_permute)

    @profile
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
            raise IndexError

        if number_of_items_to_permute == 1:
            if index == 0:
                return list_to_permute
            else:
                raise IndexError("Cannot have non-zero index when given list is contains only one element")

        previous_remainder = index
        current_offsets = list(range(number_of_items_to_permute))

        #print(f"generating permutation for index {index}")

        for i in range(number_of_items_to_permute):
            index_in_remaining_list, previous_remainder = self._get_indicies(previous_remainder, number_of_items_to_permute - i)
            index_in_complete_list = current_offsets[index_in_remaining_list]
            #print(f"{index_in_remaining_list=} {previous_remainder=} {index_in_complete_list=}")
            current_offsets.pop(index_in_remaining_list)
            self._result[i] = list_to_permute[index_in_complete_list]

        return self._result

    def mark_last_permutation_as_invalid(
            self,
            first_invalid_item_in_permutation: int) -> None:
        # given the assumption that the `first_invalid_item_in_permutation` will
        #   occur at the first index possible (ie, first time that we end up with
        #   --a--b (a<b)), then we only need to count until a is no longer in the
        #   same position. this is equivalent to incrementing by ...UNKNOWN.
        # this assumption only holds for precedes constraints, i think?
        increment_by = self._factorial_cache[self._number_of_items_to_permute - first_invalid_item_in_permutation - 1]
        self._index += increment_by
        if self._logging:
            print(f"pruning from {first_invalid_item_in_permutation=}, {increment_by=}")

        # this service works by counting from 0 to n!, where n is the number of items
        #   for i in n
        #     divmod(

    @profile
    def _get_indicies(self, index: int, number_of_items_to_permute: int) -> tuple[int, int]:
        number_of_items_to_permute_excluding_first_factorial = self._factorial_cache[number_of_items_to_permute - 1]

        return divmod(index, number_of_items_to_permute_excluding_first_factorial)
