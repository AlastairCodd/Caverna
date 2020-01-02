from automated_tests.mocks.mock_player import MockPlayer
from automated_tests.mocks.mock_tile import MockTile
from automated_tests.business_logic_tests.action_tests.get_a_baby_dwarf_action_tests.given_a_getababydwarfaction import \
    Given_A_GetABabyDwarfAction
from buisness_logic.effects.population_effects import IncreasePopulationCapacityEffect
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_tile import BaseTile


class Test_When_Number_Of_Dwarves_Is_Less_Than_Default_And_Less_Than_Capacity(Given_A_GetABabyDwarfAction):
    def because(self):
        starting_tile: BaseTile = MockTile(effects=[IncreasePopulationCapacityEffect(2)])
        additional_tile: BaseTile = MockTile(effects=[IncreasePopulationCapacityEffect(1)])
        self._mockPlayer: Player = MockPlayer(2, tiles=[starting_tile, additional_tile])

        self._result: ResultLookup[int] = self.SUT.invoke(self._mockPlayer, None, None)

    def test_then_result_should_not_be_none(self):
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self):
        self.assertTrue(self._result.flag)

    def test_then_player_should_have_three_dwarves(self):
        self.assertEqual(len(self._mockPlayer.dwarves), 3)