from math import floor
from typing import Generator, List, TypeVar, Dict

T = TypeVar("T")


class SetPartitionForge(object):
    def generate_set_partitions(
            self,
            keys: List[int],
            set_to_partition: List[T]) -> Generator[Dict[int, T], None, None]:
        number_of_partitions: int = len(set_to_partition) ** len(keys)
        for i in range(number_of_partitions):
            yield self.generate_set_partition_for_index(
                keys,
                set_to_partition,
                i)

    def generate_set_partition_for_index(
            self,
            keys: List[int],
            set_to_partition: List[T],
            index: int) -> Dict[int, T]:
        """Generates the specific set partition identified by the given index.
        example: given 5 boxes, and set [a, b, c]:
        aabac = 00102 = 0*3^4 + 0*3^3 + 1*3^2 + 0*3^1 + 2*3^0 =  11 = index.
        ccbba = 22110 = 2*3^4 + 2*3^3 + 1*3^2 + 1*3^1 + 0*3^0 = 228 = index.

        :param keys: The boxes the set should be divided between. This must be a natural number.
        :param set_to_partition: The set to partition. This cannot be null.
        :param index: The index. This must be in the range [0, len(set_to_partition) ^ number_of_boxes)
        :return: The set partition which corresponds to the given index. This will never be null.
        """
        result: Dict[int, T] = {}
        size_of_set_to_partition = len(set_to_partition)

        for p in range(len(keys)):
            item_index: int = floor(index / (size_of_set_to_partition ** p) % size_of_set_to_partition)
            partition_element: T = set_to_partition[item_index]
            result[keys[p]] = partition_element

        return result
