from typing import List, Dict, Optional, TypeVar, Tuple
from core.exceptions.ArgumentOutOfRangeError import ArgumentOutOfRangeError

T = TypeVar('T')


class PartitionResourceValidator:

    def does_partition_store_all_resources(
            self,
            resource_layout: Dict[int, Dict[T, int]],
            current_resources: Dict[T, int],
            partition: Dict[int, Optional[T]]) -> bool:
        if resource_layout is None:
            raise ValueError("resource layout may not be null")
        if current_resources is None:
            raise ValueError("current resources may not be null")
        if partition is None:
            raise ValueError("partition may not be null")
        if len(partition) != len(resource_layout):
            raise ArgumentOutOfRangeError("partition", "resource layout")

        remaining_resources: Dict[T, int]
        excess_storage: Dict[T, int]
        remaining_resources, excess_storage = self.get_resource_remaining_and_excess(resource_layout, current_resources, partition)
        result: bool = all([x == 0 for x in remaining_resources.values()])
        return result

    def get_resource_remaining_and_excess(
            self,
            resource_layout: Dict[int, Dict[T, int]],
            current_resources: Dict[T, int],
            partition: Dict[int, Optional[T]]) -> Tuple[Dict[T, int], Dict[T, int]]:
        """

        :param resource_layout: A dictionary, keyed off tile positions, containing the T which may be stored on this tile.
        :param current_resources: The current resources that must be stored.
        :param partition: The
        :return:
        """
        if resource_layout is None:
            raise ValueError("resource layout may not be null")
        if current_resources is None:
            raise ValueError("current resources may not be null")
        if partition is None:
            raise ValueError("partition may not be null")
        if len(partition) != len(resource_layout):
            raise ArgumentOutOfRangeError("partition", "resource layout")

        remaining_resources: Dict[T, int] = dict(current_resources)
        excess_resources: Dict[T, int] = {t: 0 for t in current_resources}
        for key in partition:
            object_stored_in_current: Optional[T] = partition[key]

            if object_stored_in_current is not None:
                current_tile: Dict[T, int] = resource_layout[key]
                amount_of_resources_allowed_in_current: int = current_tile[object_stored_in_current]

                if object_stored_in_current in remaining_resources:
                    if remaining_resources[object_stored_in_current] < amount_of_resources_allowed_in_current:
                        excess_resources[object_stored_in_current] += amount_of_resources_allowed_in_current - remaining_resources[object_stored_in_current]
                        remaining_resources[object_stored_in_current] = 0
                    else:
                        remaining_resources[object_stored_in_current] -= amount_of_resources_allowed_in_current
        return remaining_resources, excess_resources
