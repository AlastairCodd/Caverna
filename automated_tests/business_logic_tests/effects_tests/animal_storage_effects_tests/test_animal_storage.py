from datetime import datetime
from math import floor
from sys import path
from typing import List, Generator, Union, Dict, Iterable, Tuple, TextIO
from buisness_logic.validators.partition_resource_validator import PartitionResourceValidator
from common.forges.integer_partition_forge import IntegerPartitionForge
from common.services.integer_partition_permutation_forge import IntegerPartitionPermutationForge
from core.enums.caverna_enums import ResourceTypeEnum


class SuccessFailLogger(object):
    success: str = "success"
    failure: str = "failure"
    max_file_line_count: int = 1000000

    def __init__(self, success_file_path: str, fail_file_path: str) -> None:
        self._file_path: Dict[str, str] = {self.success: success_file_path, self.failure: fail_file_path}
        self._file_count: Dict[str, int] = {self.success: 0, self.failure: 0}
        self._file_line_count: Dict[str, int] = {self.success: 0, self.failure: 0}

        for file in self._file_path:
            while path.is_file(f"{self._file_path[file]}_{self._file_count[file]:0<3}.txt"):
                self._file_line_count[file] += 1

        success_file: TextIO = open(f"{success_file_path}_{self._file_count[self.success]:0<3}.txt", "a")
        failure_file: TextIO = open(f"{fail_file_path}_{self._file_count[self.failure]:0<3}.txt", "a")

        self._files: Dict[str, TextIO] = {self.success: success_file, self.failure: failure_file}

    def log(
            self,
            message: str,
            log_to_success: bool = False,
            log_to_fail: bool = False,
            log_to_output: bool = False) -> None:
        time = str(datetime.now())
        if log_to_fail:
            if message.isspace():
                self._files[self.failure].write("\n")
            self._files[self.failure].write(f"{time}    {message}\n")
            self._file_line_count[self.failure] += 1

        if log_to_success:
            if message.isspace():
                self._files[self.success].write("\n")
            self._files[self.success].write(f"{time}    {message}\n")
            self._file_line_count[self.success] += 1

        if log_to_output:
            if message.isspace():
                print()
            else:
                if log_to_fail and not log_to_success:
                    print(f"{time}  [FAI]  {message}")
                elif log_to_success and not log_to_fail:
                    print(f"{time}  [SUC]  {message}")
                else:
                    print(f"{time} [VRB] {message}")

    def close_files(self):
        for file in self._files.values():
            file.close()

    def check_file_length_and_update(self):
        for file in self._file_line_count:
            if self._file_line_count[file] >= self.max_file_line_count:
                self._files[file].close()
                self._file_count[file] += 1
                self._file_line_count[file] = 0
                self._files[file] = open(f"{self._file_path[file]}_{self._file_count[file]:0>3}.txt", "w")
                print(self._files[file].name)

    def split_files(self):
        file_type: str
        for file_type in [self.success, self.failure]:
            file: TextIO = open(self._file_path[file_type] + ".txt", "r")
            for line in file:
                self._file_line_count[file_type] += 1
                self._files[file_type].write(line)
                self.check_file_length_and_update()


class Investigation(object):
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

    def main(self, max_for_resource: int = 5, max_per_tile: int = 3, number_of_tiles: int = 5, start_possibility: int = 1) -> None:
        number_of_resource_possibilities: int = (max_for_resource + 1) ** len(self._animals)

        logger: SuccessFailLogger = SuccessFailLogger(
            f"{max_for_resource}_{max_per_tile}_{number_of_tiles}_success",
            f"{max_for_resource}_{max_per_tile}_{number_of_tiles}_failure"
        )

        logger.split_files()

        logger.log(f"number of resource possibilities: {number_of_resource_possibilities}\n", True, True)

        try:
            for i in range(start_possibility, number_of_resource_possibilities):
                resources_per_animal: Dict[ResourceTypeEnum, int] = {
                    ResourceTypeEnum.sheep:  floor((i / (max_for_resource + 1) ** 0)) % (max_for_resource + 1), #3
                    ResourceTypeEnum.boar:   floor((i / (max_for_resource + 1) ** 1)) % (max_for_resource + 1), #1
                    ResourceTypeEnum.donkey: floor((i / (max_for_resource + 1) ** 2)) % (max_for_resource + 1), #3
                    ResourceTypeEnum.cow:    floor((i / (max_for_resource + 1) ** 3)) % (max_for_resource + 1)
                }

                logger.log(" --- new resources --- ", True, True, True)
                animal: ResourceTypeEnum
                amount: int
                resource_line: str = ""
                for (animal, amount) in resources_per_animal.items():
                    resource_line += f"{animal.name}: {amount}  "
                resource_line += "\n"
                logger.log(resource_line, True, True, True)

                for resource_layout in self.generate_resource_layouts(resources_per_animal, max_per_tile, number_of_tiles):
                    evaluated_partitions: Iterable[Tuple[bool, List[Union[ResourceTypeEnum, None]], Dict[ResourceTypeEnum, int], Dict[ResourceTypeEnum, int]]] = \
                        self.check_resource_layout_against_possible_set_partitions(resource_layout, resources_per_animal)

                    has_header_been_added_to_successful_output: bool = False
                    has_header_been_added_to_failure_output: bool = False

                    self.log_header(resource_layout, logger, log_to_output=True)

                    for (success, partition, remaining, excess) in evaluated_partitions:
                        partition_line: str = "".ljust(8)
                        tile: Union[ResourceTypeEnum, None]
                        for tile in partition:
                            if tile is None:
                                partition_line += "_".ljust(8)
                            else:
                                partition_line += tile.name.ljust(8)

                        if success:
                            if not has_header_been_added_to_successful_output:
                                has_header_been_added_to_successful_output = True
                                self.log_header(resource_layout, logger, log_to_success=True, log_to_output=False)

                            animal_count: int = 0
                            partition_line += f"\texcess: {{"
                            for (animal, amount) in excess.items():
                                animal_count += 1
                                if amount != 0:
                                    partition_line += f"{animal.name}: {amount}"
                                    if animal_count != len(excess):
                                        partition_line += ", "
                            partition_line += "}"

                            logger.log(partition_line, log_to_success=True, log_to_output=True)

                        else:
                            if not has_header_been_added_to_failure_output:
                                has_header_been_added_to_failure_output = True
                                self.log_header(resource_layout, logger, log_to_fail=True, log_to_output=False)

                            animal_count: int = 0
                            partition_line += f"\tremaining: {{"
                            for (animal, amount) in remaining.items():
                                animal_count += 1
                                if amount != 0:
                                    partition_line += f"{animal.name}: {amount}"
                                    if animal_count != len(remaining):
                                        partition_line += ", "
                            partition_line += "}"

                            logger.log(partition_line, log_to_fail=True, log_to_output=True)
        except KeyboardInterrupt:
            logger.close_files()

    def check_resource_layout_against_possible_set_partitions(
            self,
            resource_layout: List[Dict[ResourceTypeEnum, int]],
            current_resources: Dict[ResourceTypeEnum, int]) \
            -> Iterable[Tuple[bool, List[Union[ResourceTypeEnum, None]], Dict[ResourceTypeEnum, int], Dict[ResourceTypeEnum, int]]]:
        """Checks the provided resource layout against all possible set partitions,
        and returns the ones which are able to store the provided resources.

        :param resource_layout: A list of dictionaries, each of which indicates how many of each resource may be stored in this set. This cannot be null.
        :param current_resources: A dictionary which says how many of each animal is attempting to be stored. This cannot be null.
        :returns: A list containing all set partitions (list with same length as resource layout, with entries matching which resource type holds this
        partition. This will never be null, but may be empty.
        """
        for partition in self.generate_set_partitions(len(resource_layout)):
            remaining, excess = self._partitionResourceValidator.get_resource_remaining_and_excess(resource_layout, current_resources, partition)
            success: bool = all([x == 0 for x in remaining.values()])
            yield (success, partition, remaining, excess)

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

    def log_header(
            self,
            resource_layout: List[Dict[ResourceTypeEnum, int]],
            logger: SuccessFailLogger,
            log_to_success: bool = False,
            log_to_fail: bool = False,
            log_to_output: bool = True):

        logger.log(" --- new resource layout ---", log_to_success, log_to_fail, log_to_output)
        for animal in self._animals:
            new_line: str = f"{animal.name}:".ljust(8)
            for tile in resource_layout:
                new_line += str(tile[animal]).ljust(8)
            logger.log(new_line, log_to_success, log_to_fail, log_to_output)


if __name__ == '__main__':
    invest = Investigation()
    invest.main(3, start_possibility=56)
