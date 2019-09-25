from typing import Dict, List, Iterable, Tuple, Union

from buisness_logic.validators.partition_resource_validator import PartitionResourceValidator
from core.enums.caverna_enums import ResourceTypeEnum


class ResourceLayoutExhaustiveChecker(object):

    def __init__(self):
        self._partitionResourceValidator: PartitionResourceValidator = PartitionResourceValidator()

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
