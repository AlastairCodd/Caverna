from automated_tests.business_logic_tests.action_tests.get_a_baby_dwarf_action_tests.MockPlayer import MockPlayer
from automated_tests.business_logic_tests.action_tests.get_a_baby_dwarf_action_tests.MockTile import MockTile
from automated_tests.business_logic_tests.action_tests.get_a_baby_dwarf_action_tests.given_a_getababydwarfaction import \
    Given_A_GetABabyDwarfAction
from buisness_logic.effects.population_effects import IncreasePopulationCapacityEffect
from common.entities.player import Player
from core.baseClasses.base_tile import BaseTile


class Test_When_Number_Of_Dwarves_Is_Less_Than_Default_And_Less_Than_Capacity(Given_A_GetABabyDwarfAction):
    def because(self):
        starting_tile: BaseTile = MockTile(effects=[IncreasePopulationCapacityEffect(2)])
        additional_tile: BaseTile = MockTile(effects=[IncreasePopulationCapacityEffect(1)])
        self._mockPlayer: Player = MockPlayer(tiles=[starting_tile, additional_tile])

        self._result: bool = self.SUT.invoke(self._mockPlayer, None)

    def test_Then_Result_Should_Be_True(self):
        self.assertTrue(self._result)

    def test_Then_Player_Should_Have_Three_Dwarves(self):
        self.assertEqual(len(self._mockPlayer.dwarves), 3)