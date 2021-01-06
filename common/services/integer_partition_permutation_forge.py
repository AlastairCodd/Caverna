from typing import List, Generator, Dict, Iterable, Tuple, cast


class IntegerPartitionPermutationForge(object):
    def generate_permutation(
            self,
            partition: List[int],
            number_of_tiles: int) -> Generator[List[int], None, None]:
        """Permutes the given partition across "number_of_tiles" spaces.

        :param partition: The partition of some integer to be permuted. This cannot be null, and its length must be less than "number_of_tiles"
        :param number_of_tiles: The number of possible spaces to permute the partition over. This must be greater than zero.
        :return: A generator which provides all permutations of the partition. This will never be null, and will yield at least one item.
        """
        if partition is None:
            raise ValueError("partition may not be null")
        if len(partition) > number_of_tiles:
            raise ValueError("cannot fill x tiles with more than x items")
        padded_partition: List[int] = partition + [0 for _ in range(number_of_tiles - len(partition))]
        index_to_count_dictionary: Dict[int, int] = {}
        for index in padded_partition:
            index_to_count_dictionary[index] = index_to_count_dictionary.setdefault(index, 0) + 1

        dict_as_tuple_list: List[Tuple[int, int]] = cast(List[Tuple[int, int]], list(list(index_to_count_dictionary.items())))

        return self._recurse(dict_as_tuple_list)

    def _recurse(
            self,
            integer_counts: List[Tuple[int, int]],
            current_index: int = 0) -> Generator[List[int], None, None]:
        """Recurses through integer counts, and returns all permutations of elements which have index >= "current_index"

        :param integer_counts: The number of times each integer appears in the permutation. This must be longer than current_index.
        :param current_index: The current index, which will be permuted into each possible permutation of elements which have index > "current_index".
        :returns: All possible permutations of elements with index >= "current_index". This will never be null.
        """
        # result = [0]
        # result = [2,2,0],[2,0,2],[0,2,2]
        # result = [1,2,2,0],[1,2,0,2],[1,0,2,2]
        #          [2,1,2,0],[2,1,0,2],[0,1,2,2]
        #          [2,2,1,0],[2,0,1,2],[0,2,1,2]
        #          [2,2,0,1],[2,0,2,1],[0,2,2,1]
        if not current_index < len(integer_counts):
            raise IndexError(f"current_index {current_index} must be less than integer count length {len(integer_counts)}")

        count_for_current_index: int = integer_counts[current_index][1]
        count_for_remaining_indices: int = 0

        if current_index + 1 < len(integer_counts):
            count_for_remaining_indices = sum(map(lambda t: t[1], integer_counts[current_index + 1:]))

        possible_positions: Iterable[List[int]] = list(self.generate_integer_positions(
            count_for_current_index,
            count_for_current_index + count_for_remaining_indices - 1))
        for position in possible_positions:
            # [1, 3]
            remaining_integer_recursion_result: Iterable[List[int]] = [[]]
            if current_index + 1 < len(integer_counts):
                remaining_integer_recursion_result = self._recurse(integer_counts, current_index + 1)

            for r in remaining_integer_recursion_result:
                result: List[int] = [integer_counts[current_index][0] for _ in range(count_for_current_index + count_for_remaining_indices)]
                other_indices: List[int] = [i for i in range(count_for_current_index + count_for_remaining_indices) if i not in position]
                for i in range(count_for_remaining_indices):
                    result[other_indices[i]] = r[i]
                yield result

    def generate_integer_positions(
            self,
            integer_count: int,
            max_index: int,
            min_index: int = 0) -> Generator[List[int], None, None]:
        # integer_position = [0,1]
        # integer_position = [0,1],[0,2],[0,3],[1,2],[1,3],[2,3]
        # integer_position = [0],[1],[2],[3],[4]
        if max_index < min_index:
            raise ValueError(f"max index must be greater than or equal to min index ({max_index} >= {min_index})")
        for x in range(min_index, max_index + 2 - integer_count):
            remaining_integer_recursion_result: Iterable[List[int]] = [[]]

            if integer_count > 1:
                remaining_integer_recursion_result = self.generate_integer_positions(integer_count - 1, max_index, x + 1)

            for recursion_result in remaining_integer_recursion_result:
                result: List[int] = [x] + recursion_result
                yield result

    def shuffle_in(self, integer: int, integer_position: List[int], current_permutation: List[int]) -> List[int]:
        """Inserts the given integer into the current_permuation, st the integer will end up at the integer_positions
        :param integer: The integer to be inserted into the current_permutation.
        :param integer_position: A list containing the positions the integer will end up. This cannot be null, and none of the values can be greater than the total count of
        current_permutation and integer_position.
        :param current_permutation: The current permutation the integer will be inserted into. This cannot be null.
        :returns: A new list of integers, of length current_permutation plus integer_position. This will never be null.
        """
        j: int = 0
        result: List[int] = []
        result_total_len: int = len(current_permutation) + len(integer_position)

        if len(current_permutation) == 0:
            return [integer for _ in range(len(integer_position))]

        for i in range(len(integer_position)):
            if not 0 <= integer_position[i] < result_total_len:
                raise IndexError("integer position cannot be outside range")

            k: int = integer_position[i] - i
            if k == -1:
                result += [integer]
            else:
                subset_left: List[int] = current_permutation[j:k]
                result = result + subset_left + [integer]
            j = k

        subset_right: List[int] = current_permutation[j:]
        result += subset_right
        return result
