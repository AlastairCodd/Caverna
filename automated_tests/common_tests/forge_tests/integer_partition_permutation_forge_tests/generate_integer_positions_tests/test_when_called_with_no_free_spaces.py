from typing import List

from automated_tests.common_tests.forge_tests.integer_partition_permutation_forge_tests.given_a_integer_partition_permutation_forge import \
    Given_A_IntegerPartitionPermutationForge


class Test_When_Called_With_No_Free_Space(Given_A_IntegerPartitionPermutationForge):
    def because(self) -> None:
        self._result: List[List[int]] = list(self.SUT.generate_integer_positions(2, 1))
        
    def test_then_result_should_be_expected(self) -> None:
        self.assertListEqual([[0,1]], self._result)
