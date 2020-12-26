from automated_tests.business_logic_tests.action_tests.get_a_baby_dwarf_action_tests.given_a_getababydwarfaction import \
    Given_A_GetABabyDwarfAction
from automated_tests.mocks.mock_player import MockPlayer
from automated_tests.mocks.mock_tile import MockTile
from buisness_logic.effects.population_effects import IncreasePopulationCapacityEffect
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_tile import BaseTile
from core.services.base_player_service import BasePlayerService


class test_when_number_of_dwarves_is_less_than_default_and_less_than_capacity(Given_A_GetABabyDwarfAction):
    def because(self):
        additional_tile: BaseTile = MockTile(effects=[IncreasePopulationCapacityEffect(1)])
        self._player: BasePlayerService = MockPlayer()
        self._player.tiles[28].set_tile(additional_tile)

        # noinspection PyTypeChecker
        self._result: ResultLookup[int] = self.SUT.invoke(
            self._player,
            None,
            None)

    def test_then_result_should_not_be_none(self):
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self):
        self.assertTrue(self._result.flag)

    def test_then_player_should_have_three_dwarves(self):
        self.assertEqual(len(self._player.dwarves), 3)
