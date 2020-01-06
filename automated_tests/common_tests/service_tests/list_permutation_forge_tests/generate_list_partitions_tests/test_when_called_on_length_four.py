from typing import List

from automated_tests.common_tests.service_tests.list_permutation_forge_tests.given_a_listpermutationforge import Given_A_ListPermutationForge


class Test_When_Called_On_Length_Four(Given_A_ListPermutationForge):
    def because(self) -> None:
        self._expected_permutations: List[List[int]] = [
            [1, 2, 3, 4],
            [1, 2, 4, 3],
            [1, 3, 2, 4],
            [1, 3, 4, 2],
            [1, 4, 2, 3],
            [1, 4, 3, 2],
            [2, 1, 3, 4],
            [2, 1, 4, 3],
            [2, 3, 1, 4],
            [2, 3, 4, 1],
            [2, 4, 1, 3],
            [2, 4, 3, 1],
            [3, 1, 2, 4],
            [3, 1, 4, 2],
            [3, 2, 1, 4],
            [3, 2, 4, 1],
            [3, 4, 1, 2],
            [3, 4, 2, 1],
            [4, 1, 2, 3],
            [4, 1, 3, 2],
            [4, 2, 1, 3],
            [4, 2, 3, 1],
            [4, 3, 1, 2],
            [4, 3, 2, 1],
        ]
        self._result: List[List[int]] = list(self.SUT.generate_list_partitions([1, 2, 3, 4]))

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_should_contain_expected_permutations(self) -> None:
        for permutation in self._expected_permutations:
            with self.subTest(permutation=permutation):
                self.assertIn(permutation, self._result)
