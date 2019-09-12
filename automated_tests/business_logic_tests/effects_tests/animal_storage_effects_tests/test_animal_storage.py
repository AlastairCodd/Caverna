from math import floor
from typing import List, Generator, Union, Dict, Iterable, Tuple
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

    def main(self, max_for_resource: int = 5, max_per_tile: int = 3, number_of_tiles: int = 5) -> None:
        number_of_resource_possibilities: int = (max_for_resource + 1) ** len(self._animals)
        print(number_of_resource_possibilities)
        print()
        for i in range(1, number_of_resource_possibilities):
            resources_per_animal: Dict[ResourceTypeEnum, int] = {
                ResourceTypeEnum.sheep: floor((i / (max_for_resource + 1) ** 0)) % (max_for_resource + 1),
                ResourceTypeEnum.boar: floor((i / (max_for_resource + 1) ** 1)) % (max_for_resource + 1),
                ResourceTypeEnum.donkey: floor((i / (max_for_resource + 1) ** 2)) % (max_for_resource + 1),
                ResourceTypeEnum.cow: floor((i / (max_for_resource + 1) ** 3)) % (max_for_resource + 1)
            }
            animal: ResourceTypeEnum
            amount: int
            for (animal, amount) in resources_per_animal.items():
                print(f"{animal.name}:\t{amount}")
            print()

            for resource_layout in self.generate_resource_layouts(resources_per_animal, max_per_tile, number_of_tiles):
                print(" --- new resource layout ---")
                for animal in self._animals:
                    print(f"{animal.name}:\t", end="")
                    for tile in resource_layout:
                        print(f"{tile[animal]}\t", end="")
                    print()

                successful_partitions: List[Tuple[List[Union[ResourceTypeEnum, None]], Dict[ResourceTypeEnum, int]]] = \
                    list(self.check_resource_layout_against_possible_set_partitions(resource_layout, resources_per_animal))
                if any(successful_partitions):
                    for (partition, excess) in successful_partitions:
                        tile: Union[ResourceTypeEnum, None]
                        for tile in partition:
                            if tile is None:
                                print("_\t\t", end="")
                            else:
                                if tile is ResourceTypeEnum.cow:
                                    print(f"cow\t\t", end="")
                                else:
                                    print(f"{tile.name}\t", end="")
                        print(f"excess: {{", end="")
                        print(f"sheep: {excess[ResourceTypeEnum.sheep]}, ", end="")
                        print(f"boar: {excess[ResourceTypeEnum.boar]}, ", end="")
                        print(f"donkey: {excess[ResourceTypeEnum.donkey]}, ", end=""),
                        print(f"cow: {excess[ResourceTypeEnum.cow]}}}")
                else:
                    print("no successful allocations")
                print()

    def check_resource_layout_against_possible_set_partitions(
            self,
            resource_layout: List[Dict[ResourceTypeEnum, int]],
            current_resources: Dict[ResourceTypeEnum, int]) \
            -> Iterable[Tuple[List[Union[ResourceTypeEnum, None]], Dict[ResourceTypeEnum, int]]]:
        """Checks the provided resource layout against all possible set partitions,
        and returns the ones which are able to store the provided resources.

        :param resource_layout: A list of dictionaries, each of which indicates how many of each resource may be stored in this set. This cannot be null.
        :param current_resources: A dictionary which says how many of each animal is attempting to be stored. This cannot be null.
        :returns: A list containing all set partitions (list with same length as resource layout, with entries matching which resource type holds this
        partition. This will never be null, but may be empty.
        """
        for partition in self.generate_set_partitions(len(resource_layout)):
            excess = self._partitionResourceValidator.get_resource_excess(resource_layout, current_resources, partition)
            if all([x == 0 for x in excess.values()]):
                yield (partition, excess)

    def generate_resource_layouts(
            self,
            resources_per_animal: Dict[ResourceTypeEnum, int],
            max_resources_per_tile: int,
            number_of_tiles: int) \
            -> Generator[List[Dict[ResourceTypeEnum, int]], None, None]:
        sheep_partitions: Iterable[List[int]] = self._integerPartitionForge \
            .generate_integer_partitions(resources_per_animal[ResourceTypeEnum.sheep])
        for sheep_partition in sheep_partitions:
            if not self._are_partition_dimensions_valid(sheep_partition, max_resources_per_tile, number_of_tiles):
                continue
            permuted_sheep_partitions: Iterable[List[int]] = self._integerPartitionPermutationForge \
                .generate_permutation(sheep_partition, number_of_tiles)
            for permuted_sheep_partition in permuted_sheep_partitions:

                boar_partitions: Iterable[List[int]] = self._integerPartitionForge \
                    .generate_integer_partitions(resources_per_animal[ResourceTypeEnum.boar])
                for boar_partition in boar_partitions:
                    if not self._are_partition_dimensions_valid(boar_partition, max_resources_per_tile, number_of_tiles):
                        continue
                    permuted_boar_partitions: Iterable[List[int]] = self._integerPartitionPermutationForge \
                        .generate_permutation(boar_partition, number_of_tiles)
                    for permuted_boar_partition in permuted_boar_partitions:

                        donkey_partitions: Iterable[List[int]] = self._integerPartitionForge \
                            .generate_integer_partitions(resources_per_animal[ResourceTypeEnum.donkey])
                        for donkey_partition in donkey_partitions:
                            if not self._are_partition_dimensions_valid(donkey_partition, max_resources_per_tile, number_of_tiles):
                                continue
                            permuted_donkey_partitions: Iterable[List[int]] = self._integerPartitionPermutationForge \
                                .generate_permutation(donkey_partition, number_of_tiles)
                            for permuted_donkey_partition in permuted_donkey_partitions:

                                cow_partitions: Iterable[List[int]] = self._integerPartitionForge \
                                    .generate_integer_partitions(resources_per_animal[ResourceTypeEnum.cow])
                                for cow_partition in cow_partitions:
                                    if not self._are_partition_dimensions_valid(cow_partition, max_resources_per_tile, number_of_tiles):
                                        continue
                                    permuted_cow_partitions: Iterable[List[int]] = self._integerPartitionPermutationForge \
                                        .generate_permutation(cow_partition, number_of_tiles)
                                    for permuted_cow_partition in permuted_cow_partitions:

                                        result: List[Dict[ResourceTypeEnum, int]] = []
                                        for i in range(number_of_tiles):
                                            result.append({
                                                ResourceTypeEnum.sheep: permuted_sheep_partition[i],
                                                ResourceTypeEnum.boar: permuted_boar_partition[i],
                                                ResourceTypeEnum.donkey: permuted_donkey_partition[i],
                                                ResourceTypeEnum.cow: permuted_cow_partition[i],
                                            })
                                        yield result

    def _are_partition_dimensions_valid(
            self,
            partition: List[int],
            max_resources_per_tile: int,
            number_of_tiles: int) -> bool:
        result: bool = len(partition) <= number_of_tiles and all(x for x in partition if x < max_resources_per_tile)
        return result

    def generate_set_partitions(self, number_of_tiles: int) -> Generator[List[Union[ResourceTypeEnum, None]], None, None]:
        number_of_partitions: int = len(self._animals_or_none) ** number_of_tiles
        for i in range(number_of_partitions):
            yield self.generate_set_partition_for_index(number_of_tiles, i)

    def generate_set_partition_for_index(self, number_of_tiles: int, index: int) -> List[Union[ResourceTypeEnum, None]]:
        result: List[Union[ResourceTypeEnum, None]] = []
        for p in range(number_of_tiles):
            number_of_animals = len(self._animals_or_none)
            animal_index: int = floor(index / (number_of_animals ** p) % number_of_animals)
            animal: Union[ResourceTypeEnum, None] = self._animals_or_none[animal_index]
            result.append(animal)

        return result


if __name__ == '__main__':
    invest = Investigation()
    invest.main()
