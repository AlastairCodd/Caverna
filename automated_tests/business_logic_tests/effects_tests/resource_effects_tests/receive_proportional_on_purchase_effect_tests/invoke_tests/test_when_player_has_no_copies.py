from typing import Dict

from automated_tests.business_logic_tests.effects_tests.resource_effects_tests.receive_proportional_on_purchase_effect_tests\
    .given_a_ReceiveProportionalOnPurchaseEffect import Given_A_ReceiveProportionalOnPurchaseEffect
from automated_tests.business_logic_tests.service_tests.mock_player import MockPlayer
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class Test_When_player_has_no_copies(Given_A_ReceiveProportionalOnPurchaseEffect):
    def because(self) -> None:
        self._player_repository: BasePlayerRepository = MockPlayer()

        self._resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: 1,
            ResourceTypeEnum.stone: 1,
            ResourceTypeEnum.ore: 2,
        }
        self._player_repository.give_resources(self._resources)

        self._result: bool = self.SUT.invoke(self._player_repository)
        
    def test_then_result_should_be_true(self) -> None:
        self.assertTrue(self._result)

    def test_then_player_should_have_expected_resources(self) -> None:
        for resource in self._resources:
            with self.subTest(resource=resource):
                self.assertEqual(self._player_repository.resources[resource], self._resources[resource])
