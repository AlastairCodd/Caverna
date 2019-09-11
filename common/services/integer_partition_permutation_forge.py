from typing import List, Generator, Dict


class IntegerPartitionPermutationForge():
    def generate_permutation(self, partition: List[int], number_of_tiles: int) -> Generator[List[int], None, None]:
        # partition = [1,2,2], n_o_t = 5
        if partition is None:
            raise ValueError("partition may not be null")
        if len(partition) > number_of_tiles:
            raise ValueError("cannot fill x tiles with more than x items")
        # p_part = [1,2,2,0,0]
        padded_partition: List[int] = partition + [0 for _ in range(number_of_tiles - len(partition))]
        index_to_count_dictionary: Dict[int, int] = {}
        for index in padded_partition:
            index_to_count_dictionary[index] = index_to_count_dictionary.setdefault(index, 0) + 1

        result: List[int] = []

        # integer_position = [0,1]
        # integer_position = [0,1],[0,2],[0,3],[1,2],[1,3],[2,3]
        # integer_position = [0],[1],[2],[3],[4]

        # result = [0,0]
        # result = [2,2,0,0],[2,0,2,0],[2,0,0,2],[0,2,2,0],[0,2,0,2],[0,0,2,2]
        # result = [1,2,2,0,0],[1,2,0,2,0],[1,2,0,0,2],[1,0,2,2,0],[1,0,2,0,2],[1,0,0,2,2],
        #          [2,1,2,0,0],[2,1,0,2,0],[2,1,0,0,2],[0,1,2,2,0],[0,1,2,0,2],[0,1,0,2,2],
        #          [2,2,1,0,0],[2,0,1,2,0],[2,0,1,0,2],[0,2,1,2,0],[0,2,1,0,2],[0,0,1,2,2],
        #          [2,2,0,1,0],[2,0,2,1,0],[2,0,0,1,2],[0,2,2,1,0],[0,2,0,1,2],[0,0,2,1,2],
        #          [2,2,0,0,1],[2,0,2,0,1],[2,0,0,2,1],[0,2,2,0,1],[0,2,0,2,1],[0,0,2,2,1]
        for index, count in index_to_count_dictionary.items():
            pass

    def shuffle_in(self, integer: int, integer_position: List[int], current_permutation: List[int]) -> List[int]:
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
