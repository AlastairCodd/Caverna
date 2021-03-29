from typing import Dict, List, Iterable, Tuple, Optional

from buisness_logic.validators.partition_resource_validator import PartitionResourceValidator
from common.forges.set_partition_forge import SetPartitionForge
from core.enums.caverna_enums import ResourceTypeEnum
from core.services.resource_layout_check_service import ResourceLayoutCheckService


class ResourceLayoutExhaustiveChecker(ResourceLayoutCheckService):
    def __init__(self):
        self._partition_resource_validator: PartitionResourceValidator = PartitionResourceValidator()
        self._set_partition_forge: SetPartitionForge = SetPartitionForge()
        self._animals_or_none: List[Optional[ResourceTypeEnum]] = [
            ResourceTypeEnum.sheep,
            ResourceTypeEnum.donkey,
            ResourceTypeEnum.cow,
            ResourceTypeEnum.boar]

    def check_resource_layout(
            self,
            resource_layout: Dict[int, Dict[ResourceTypeEnum, int]],
            current_resources: Dict[ResourceTypeEnum, int]) \
            -> Iterable[Tuple[
                    bool,
                    Dict[int, Optional[ResourceTypeEnum]],
                    Dict[ResourceTypeEnum, int],
                    Dict[ResourceTypeEnum, int]
                ]]:
        """Checks the provided resource layout against all possible set partitions,
        and returns the ones which are able to store the provided resources.

        :param resource_layout: A list of dictionaries, each of which indicates how many of each resource may be stored in this set. This cannot be null.
        :param current_resources: A dictionary which says how many of each animal is attempting to be stored. This cannot be null.
        :returns: A list containing all set partitions (list with same length as resource layout, with entries matching which resource type holds this
        partition. This will never be null, but may be empty.
        """
        for partition in self._set_partition_forge.generate_set_partitions(
                list(resource_layout.keys()),
                self._animals_or_none):
            remaining, excess = self._partition_resource_validator\
                .get_resource_remaining_and_excess(
                    resource_layout,
                    current_resources,
                    partition)

            success: bool = all([x == 0 for x in remaining.values()])
            result: Tuple[
                    bool,
                    Dict[int, Optional[ResourceTypeEnum]],
                    Dict[ResourceTypeEnum, int],
                    Dict[ResourceTypeEnum, int]
            ] = (success, partition, remaining, excess)
            yield result
