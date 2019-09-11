from typing import List

from automated_tests.common_tests.forge_tests.integer_partition_permutation_forge_tests.given_a_integer_partition_permutation_forge import \
    Given_A_IntegerPartitionPermutationForge


class Test_When_Called(Given_A_IntegerPartitionPermutationForge):
    def because(self) -> None:
        self.result: List[int] = self.SUT.shuffle_in(2, [1, 4], [0, 1, 1, 0])

    def test_then_result_should_be_expected(self):
        self.assertListEqual([0, 2, 1, 1, 2, 0], self.result)


class Test_When_Called_Lower(Given_A_IntegerPartitionPermutationForge):
    def because(self) -> None:
        self.result: List[int] = self.SUT.shuffle_in(2, [0, 1], [0, 1, 1, 0])

    def test_then_result_should_be_expected(self):
        self.assertListEqual([2, 2, 0, 1, 1, 0], self.result)


class Test_When_Called_Upper(Given_A_IntegerPartitionPermutationForge):
    def because(self) -> None:
        self.result: List[int] = self.SUT.shuffle_in(2, [4, 5], [0, 1, 1, 0])

    def test_then_result_should_be_expected(self):
        self.assertListEqual([0, 1, 1, 0, 2, 2], self.result)