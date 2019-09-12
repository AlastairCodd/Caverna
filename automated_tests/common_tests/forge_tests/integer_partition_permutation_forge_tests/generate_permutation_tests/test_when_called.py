from typing import List

from automated_tests.common_tests.forge_tests.integer_partition_permutation_forge_tests.given_a_integer_partition_permutation_forge import \
    Given_A_IntegerPartitionPermutationForge


class Test_When_Test_When_Called(Given_A_IntegerPartitionPermutationForge):
    def because(self) -> None:
        self.maxDiff = None
        self._expected_result: List[List[int]] = [
            [1, 2, 2, 0], [1, 2, 0, 2], [1, 0, 2, 2],
            [2, 1, 2, 0], [2, 1, 0, 2], [0, 1, 2, 2],
            [2, 2, 1, 0], [2, 0, 1, 2], [0, 2, 1, 2],
            [2, 2, 0, 1], [2, 0, 2, 1], [0, 2, 2, 1]
        ]
        integer_partition: List[int] = [1, 2, 2]
        number_of_tiles: int = 4
        self._result: List[List[int]] = list(self.SUT.generate_permutation(integer_partition, number_of_tiles))
        
    def test_then_list_should_contain_expected_values(self):
        self.assertListEqual(self._expected_result, self._result)
