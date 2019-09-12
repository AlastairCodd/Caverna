from typing import List, Dict, Union, TypeVar
from core.exceptions.ArgumentOutOfRangeError import ArgumentOutOfRangeError

T = TypeVar('T')


class PartitionResourceValidator:

    def does_partition_store_all_resources(
            self,
            resource_layout: List[Dict[T, int]],
            current_resources: Dict[T, int],
            partition: List[Union[T, None]]) -> bool:
        if resource_layout is None:
            raise ValueError("resource layout may not be null")
        if current_resources is None:
            raise ValueError("current resources may not be null")
        if partition is None:
            raise ValueError("partition may not be null")
        if len(partition) != len(resource_layout):
            raise ArgumentOutOfRangeError("partition", "resource layout")

        remaining_resources: Dict[T, int] = self.get_resource_excess(resource_layout, current_resources, partition)
        result: bool = all([x == 0 for x in remaining_resources.values()])
        return result

    def get_resource_excess(
            self,
            resource_layout: List[Dict[T, int]],
            current_resources: Dict[T, int],
            partition: List[Union[T, None]]) -> Dict[T, int]:
        if resource_layout is None:
            raise ValueError("resource layout may not be null")
        if current_resources is None:
            raise ValueError("current resources may not be null")
        if partition is None:
            raise ValueError("partition may not be null")
        if len(partition) != len(resource_layout):
            raise ArgumentOutOfRangeError("partition", "resource layout")

        remaining_resources: Dict[T, int] = dict(current_resources)
        for i in range(len(partition)):
            object_stored_in_current: Union[T, None] = partition[i]
            if object_stored_in_current is not None:
                amount_of_resources_allowed_in_current: int = resource_layout[i][object_stored_in_current]
                if object_stored_in_current in remaining_resources:
                    if remaining_resources[object_stored_in_current] < amount_of_resources_allowed_in_current:
                        remaining_resources[object_stored_in_current] = 0
                    else:
                        remaining_resources[object_stored_in_current] -= amount_of_resources_allowed_in_current
        return remaining_resources
