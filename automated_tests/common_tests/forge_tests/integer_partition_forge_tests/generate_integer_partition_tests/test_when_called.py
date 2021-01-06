from typing import List

from automated_tests.common_tests.forge_tests.integer_partition_forge_tests.given_an_integer_partition_forge import Given_An_IntegerPartitionForge


class Test_When_Called(Given_An_IntegerPartitionForge):
    def because(self) -> None:
        self.result: List[List[int]] = list(self.SUT.generate_integer_partitions(5))

    def test_then_result_should_not_be_empty(self) -> None:
        self.assertFalse(len(self.result) == 0)

    def test_then_result_should_contain_expected(self) -> None:
        expected_result = [
            [5],
            [4, 1],
            [3, 2], [3, 1, 1],
            [2, 2, 1], [2, 1, 1, 1],
            [1, 1, 1, 1, 1]]
        self.assertListEqual(expected_result, self.result)


class Test_When_Integer_Is_6(Given_An_IntegerPartitionForge):
    def because(self) -> None:
        self.result: List[List[int]] = list(self.SUT.generate_integer_partitions(6))
        self.expected_result: List[List[int]] = [
            [6],
            [5, 1],
            [4, 2], [4, 1, 1],
            [3, 3], [3, 2, 1], [3, 1, 1, 1],
            [2, 2, 2], [2, 2, 1, 1], [2, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1]
        ]

    def test_then_result_should_not_be_empty(self) -> None:
        self.assertFalse(len(self.result) == 0)

    def test_then_result_should_contain_expected(self) -> None:
        self.assertListEqual(self.expected_result, self.result)