from math import floor
from typing import List, Generator, Union, Dict, Iterable
from buisness_logic.validators.partition_resource_validator import PartitionResourceValidator
from common.forges.integer_partition_forge import IntegerPartitionForge
from common.services.integer_partition_permutation_forge import IntegerPartitionPermutationForge
from core.enums.caverna_enums import ResourceTypeEnum


class Investigation():
    def __init__(self):
        self._partitionResourceValidator: PartitionResourceValidator = PartitionResourceValidator()
        self._integerPartitionForge: IntegerPartitionForge = IntegerPartitionForge()
        self._integerPartitionPermutationForge: IntegerPartitionPermutationForge = IntegerPartitionPermutationForge()
        self._animals: List[ResourceTypeEnum] = [
            ResourceTypeEnum.sheep,
            ResourceTypeEnum.boar,
            ResourceTypeEnum.donkey,
            ResourceTypeEnum.cow
        ]

        self._animals_or_none: List[Union[ResourceTypeEnum, None]] = [
            None,
            ResourceTypeEnum.sheep,
            ResourceTypeEnum.boar,
            ResourceTypeEnum.donkey,
            ResourceTypeEnum.cow
        ]

    def main(self, max_for_resource: int = 5, max_per_tile: int = 3, number_of_tiles: int = 5):
        for resource_layout in self.generate_resource_layouts(max_per_tile, number_of_tiles):
            successful_partitions: List[List[Union[ResourceTypeEnum, None]]] = \
                self.check_resource_layout_against_possible_set_partitions(resource_layout, {})

    def check_resource_layout_against_possible_set_partitions(
            self,
            resource_layout: List[Dict[ResourceTypeEnum, int]],
            current_resources: Dict[ResourceTypeEnum, int]) -> List[List[Union[ResourceTypeEnum, None]]]:
        """Checks the provided resource layout against all possible set partitions,
        and returns the ones which are able to store the provided resources.

        :param resource_layout: A list of dictionaries, each of which indicates how many of each resource may be stored in this set. This cannot be null.
        :param current_resources: A dictionary which says how many of each animal is attempting to be stored. This cannot be null.
        :returns: A list containing all set partitions (list with same length as resource layout, with entries matching which resource type holds this
        partition. This will never be null, but may be empty.
        """
        successes: List[List[Union[ResourceTypeEnum, None]]] = []
        for partition in self.generate_set_partitions(len(resource_layout)):
            if partition is self._partitionResourceValidator.does_partition_store_all_resources(resource_layout, current_resources, partition):
                successes.append(partition)
        return successes

    def generate_resource_layouts(self, max_resources_per_tile: int, number_of_tiles: int) \
            -> Generator[List[Dict[ResourceTypeEnum, int]], None, None]:
        result: List[Dict[ResourceTypeEnum, int]] = []
        integer_partitions: Iterable[List[int]] = self._integerPartitionForge.generate_integer_partitions(max_resources_per_tile)

        for animal in self._animals:
            for integer_partition in integer_partitions:
                #sheep, [3, 2, 1]
                for permutation in self._integerPartitionPermutationForge.generate_permutation(integer_partition, number_of_tiles):
                    pass

    def generate_resource_layout_for_partition(self, animal_type: ResourceTypeEnum, partition: List[int], number_of_tiles) \
            -> Generator[List[Dict[ResourceTypeEnum, int]], None, None]:
        pass

    def generate_set_partitions(self, number_of_tiles: int) -> Generator[List[Union[ResourceTypeEnum, None]], None, None]:
        number_of_partitions: int = pow(len(self._animals_or_none), number_of_tiles)
        for i in range(number_of_partitions):
            yield self.generate_set_partition_for_index(number_of_tiles, i)

    def generate_set_partition_for_index(self, number_of_tiles: int, index: int) -> List[Union[ResourceTypeEnum, None]]:
        result: List[Union[ResourceTypeEnum, None]] = []
        for p in range(number_of_tiles):
            number_of_animals = len(self._animals_or_none)
            animal_index: int = floor(index / pow(number_of_animals, p) % number_of_animals)
            animal: Union[ResourceTypeEnum, None] = self._animals_or_none[animal_index]
            result.append(animal)

        return result


if __name__ == '__main__':
    invest = Investigation()
    invest.main()
