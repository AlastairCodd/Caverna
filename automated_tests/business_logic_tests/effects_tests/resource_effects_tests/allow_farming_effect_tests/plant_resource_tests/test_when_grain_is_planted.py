from typing import Dict, List, cast

from automated_tests.business_logic_tests.effects_tests.resource_effects_tests.allow_farming_effect_tests.given_an_allow_farming_effect import \
    Given_An_AllowFarmingEffect
from automated_tests.mocks.mock_player import MockPlayer
from common.entities.result_lookup import ResultLookup
from core.enums.caverna_enums import ResourceTypeEnum


class test_when_grain_is_planted(Given_An_AllowFarmingEffect):
    def because(self) -> None:
        resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: 2,
            ResourceTypeEnum.veg: 2,
            ResourceTypeEnum.grain: 3}
        self._player: MockPlayer = MockPlayer(resources=resources)

        self._expected_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: 2,
            ResourceTypeEnum.veg: 2,
            ResourceTypeEnum.grain: 2}

        self._result: ResultLookup[bool] = self.SUT.plant_resource(self._player, ResourceTypeEnum.grain)

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_errors_should_be_empty(self) -> None:
        self.assertEqual(len(cast(List, self._result.errors)), 0)

    def test_then_sut_planted_type_should_be_expected(self) -> None:
        self.assertEqual(self.SUT.planted_resource_type, ResourceTypeEnum.grain)

    def test_then_sut_planted_amount_should_be_expected(self) -> None:
        self.assertEqual(self.SUT.planted_resource_amount, 3)

    def test_then_player_resources_should_contain_expected_resources(self) -> None:
        for resource in self._expected_resources:
            with self.subTest(resources=resource):
                self.assertIn(resource, self._player.resources)
