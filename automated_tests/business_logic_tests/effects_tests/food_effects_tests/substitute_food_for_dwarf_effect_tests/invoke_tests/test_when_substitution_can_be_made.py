from typing import List, Dict

from automated_tests.business_logic_tests.effects_tests.food_effects_tests.substitute_food_for_dwarf_effect_tests.given_a_substitute_food_for_dwarf_effect import \
    Given_A_SubstituteFoodForDwarfEffect
from core.enums.caverna_enums import ResourceTypeEnum


class test_when_substitution_can_be_made(Given_A_SubstituteFoodForDwarfEffect):
    def because(self) -> None:
        self._resources_per_dwarf: List[Dict[ResourceTypeEnum, int]] = [
            {ResourceTypeEnum.stone: 1},
            {ResourceTypeEnum.food: 1},
            {ResourceTypeEnum.food: 1},
            {ResourceTypeEnum.food: 2},
            {ResourceTypeEnum.food: 2}
        ]

        self._expected_cost_per_dwarf: List[Dict[ResourceTypeEnum, int]] = [
            {ResourceTypeEnum.stone: 1},
            {ResourceTypeEnum.food: 1},
            {ResourceTypeEnum.food: 1},
            {ResourceTypeEnum.food: 2},
            {ResourceTypeEnum.donkey: 2}
        ]

        self.SUT.invoke(self._resources_per_dwarf)
        
    def test_then_resources_per_dwarf_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._resources_per_dwarf)

    def test_then_resources_per_dwarf_should_not_be_empty(self) -> None:
        self.assertGreater(len(self._resources_per_dwarf), 0)

    def test_then_resources_per_dwarf_should_contain_expected_costs_for_dwarf(self) -> None:
        for cost_for_dwarf in self._expected_cost_per_dwarf:
            with self.subTest(costs_for_dwarf=cost_for_dwarf):
                self.assertIn(cost_for_dwarf, self._resources_per_dwarf)
