from typing import List, Tuple

from automated_tests.mocks.mock_action import MockAction
from automated_tests.business_logic_tests.service_tests.most_resources_permutation_ordering_service.given_a_most_resources_permutation_ordering_service import \
    Given_A_MostResourcesPermutationOrderingService
from automated_tests.mocks.mock_player import MockPlayer
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ResourceTypeEnum


class Test_When_There_Is_A_Single_Greatest_Resource_Permutation(Given_A_MostResourcesPermutationOrderingService):
    def because(self) -> None:
        player0: Player = MockPlayer(3, resources={ResourceTypeEnum.coin: 3})
        player1: Player = MockPlayer(3, resources={ResourceTypeEnum.coin: 3, ResourceTypeEnum.stone: 4})
        player2: Player = MockPlayer(3, resources={ResourceTypeEnum.coin: 3})
        player3: Player = MockPlayer(3, resources={ResourceTypeEnum.coin: 2, ResourceTypeEnum.wood: 1})

        permutation0: Tuple[List[BaseAction], int, Player] = ([MockAction()], 3, player0)
        permutation1: Tuple[List[BaseAction], int, Player] = ([MockAction()], 3, player1)
        permutation2: Tuple[List[BaseAction], int, Player] = ([MockAction()], 3, player2)
        permutation3: Tuple[List[BaseAction], int, Player] = ([MockAction()], 3, player3)
        successful_permutations: List[Tuple[List[BaseAction], int, Player]] = [
            permutation0,
            permutation1,
            permutation2,
            permutation3
        ]

        self._greatest_resource_permutations: List[Tuple[List[BaseAction], int, Player]] = [permutation1]

        self._result: ResultLookup[List[Tuple[List[BaseAction], int, Player]]] = self.SUT.find_best_permutation(successful_permutations)

    def test_then_result_should_not_be_none(self):
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self):
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self):
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_should_contain_expected_permutations(self):
        self.assertCountEqual(self._result.value, self._greatest_resource_permutations)
