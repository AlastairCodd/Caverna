from typing import Dict, cast

from automated_tests.business_logic_tests.effects_tests.resource_effects_tests.allow_farming_effect_tests.given_an_allow_farming_effect import \
    Given_An_AllowFarmingEffect
from automated_tests.mocks.mock_player import MockPlayer
from common.entities.result_lookup import ResultLookup
from core.enums.caverna_enums import ResourceTypeEnum


class test_when_resources_can_be_popped(Given_An_AllowFarmingEffect):
    def because(self) -> None:
        self._starting_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: 2,
            ResourceTypeEnum.veg: 2,
            ResourceTypeEnum.grain: 0}
        self._player: MockPlayer = MockPlayer(resources=self._starting_resources)

        # Veg: 1
        self.SUT.plant_resource(self._player, resource_type=ResourceTypeEnum.veg)

        # Veg: 2
        self._result: ResultLookup[int] = self.SUT.pop_resource(self._player)

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_errors_should_not_be_empty(self) -> None:
        self.assertEqual(len(cast(list,self._result.errors)), 0)

    def test_then_player_should_have_expected_amount_of_resources(self) -> None:
        for resource in self._starting_resources:
            with self.subTest(resource=resource):
                expected_amount: int = self._starting_resources[resource]
                if expected_amount == 0:
                    self.assertNotIn(resource, self._player.resources)
                else:
                    self.assertEqual(self._player.resources[resource], expected_amount)
