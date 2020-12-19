from typing import Dict, cast

from automated_tests.business_logic_tests.effects_tests.resource_effects_tests.allow_farming_effect_tests.given_an_allow_farming_effect import \
    Given_An_AllowFarmingEffect
from automated_tests.mocks.mock_player import MockPlayer
from common.entities.result_lookup import ResultLookup
from core.enums.caverna_enums import ResourceTypeEnum


class test_when_resource_type_is_null(Given_An_AllowFarmingEffect):
    def because(self) -> None:
        resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: 2,
            ResourceTypeEnum.veg: 2,
            ResourceTypeEnum.grain: 0}
        self._player: MockPlayer = MockPlayer(resources=resources)

        self._result: ResultLookup[int] = self.SUT.pop_resource(self._player)

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._result.flag)

    def test_then_result_value_should_be_none(self) -> None:
        self.assertIsNone(self._result.value)

    def test_then_result_errors_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(list,self._result.errors)), 0)
