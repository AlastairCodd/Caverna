from math import floor
from typing import Generator, List, TypeVar

T = TypeVar("T")


class SetPartitionForge(object):

    def generate_set_partitions(self, number_of_tiles: int, set_to_partition: List[T]) -> Generator[List[T], None, None]:
        number_of_partitions: int = len(set_to_partition) ** number_of_tiles
        for i in range(number_of_partitions):
            yield self.generate_set_partition_for_index(number_of_tiles, set_to_partition, i)

    def generate_set_partition_for_index(
            self,
            number_of_boxes: int,
            set_to_partition: List[T],
            index: int) -> List[T]:
        """Generates the specific set partition identified by the given index.
        example: given 5 boxes, and set [a, b, c]:
        aabac = 00102 = 0*3^4 + 0*3^3 + 1*3^2 + 0*3^1 + 2*3^0 =  11 = index.
        ccbba = 22110 = 2*3^4 + 2*3^3 + 1*3^2 + 1*3^1 + 0*3^0 = 228 = index.

        :param number_of_boxes: The number of boxes the set should be divided between. This must be a natural number.
        :param set_to_partition: The set to partition. This cannot be null.
        :param index: The index. This must be in the range [0, len(set_to_partition) ^ number_of_boxes)
        :return: The set partition which corresponds to the given index. This will never be null.
        """
        result: List[T] = []
        size_of_set_to_partition = len(set_to_partition)

        for p in range(number_of_boxes):
            item_index: int = floor(index / (size_of_set_to_partition ** p) % size_of_set_to_partition)
            partition_element: T = set_to_partition[item_index]
            result.append(partition_element)

        return result
