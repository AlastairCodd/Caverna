from typing import Dict, Optional

from automated_tests.business_logic_tests.validator_tests.partition_resource_validator_tests.given_a_partition_resource_validator import \
    Given_A_PartitionResourceValidator
from core.enums.caverna_enums import ResourceTypeEnum


class Test_When_Test_When_Partition_Does_Store_All_Resources(Given_A_PartitionResourceValidator):
    def because(self) -> None:
        a: ResourceTypeEnum = ResourceTypeEnum.sheep
        b: ResourceTypeEnum = ResourceTypeEnum.donkey
        c: ResourceTypeEnum = ResourceTypeEnum.cow
        resource_layout: Dict[int, Dict[ResourceTypeEnum, int]] = {
            1: {a: 3, b: 1, c: 4},
            2: {a: 2, b: 0, c: 1},
            3: {a: 1, b: 5, c: 3},
            4: {a: 4, b: 0, c: 4},
            5: {a: 2, b: 3, c: 3},
            6: {a: 3, b: 1, c: 4},
            7: {a: 9, b: 6, c: 5},
            8: {a: 6, b: 1, c: 0}
        }
        current_resources: Dict[ResourceTypeEnum, int] = {a: 7, b: 10, c: 4}
        partition: Dict[int, Optional[ResourceTypeEnum]] = {1: a, 2: a, 3: b, 4: None, 5: a, 6: c, 7: b, 8: None}

        self._result = self.SUT.does_partition_store_all_resources(
            resource_layout,
            current_resources,
            partition
        )

    def test_then_result_should_not_be_null(self):
        self.assertIsNotNone(self._result)

    def test_then_result_should_be_true(self):
        self.assertTrue(self._result)
