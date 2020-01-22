from typing import List, Dict, Union

from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.given_a_turn_execution_service import Given_A_TurnExecutionService
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from common.entities.weapon import Weapon
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class FakePlayer(Player):
    def __init__(self):
        Player.__init__(self)

    def get_player_choice_market_action(self, possible_items_and_costs: Dict[ResourceTypeEnum, int]) -> List[ResourceTypeEnum]:
        pass

    def get_player_choice_weapon_level(self) -> int:
        pass

    def get_player_choice_breed_animals(self, animals_which_can_reproduce: List[ResourceTypeEnum], possible_number_of_animals_to_reproduce: int) \
            -> List[ResourceTypeEnum]:
        pass

    def get_player_choice_discount(self, possible_prices: List[Dict[ResourceTypeEnum, int]], target: Union[BaseTile, Weapon]) -> Dict[ResourceTypeEnum, int]:
        pass


class Test_When_player_chooses_to_play_a_dwarf_out_of_turn_but_does_not_have_resources(Given_A_TurnExecutionService):
    def because(self) -> None:
        self._expected_errors: List[str] = ["Insufficient Resources (ruby) to perform action"]

        player: Player = FakePlayer()
        self._result: ResultLookup[Player] = self.SUT.take_turn()
        
    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._result.flag)

    def test_then_errors_should_contain_expected_errors(self) -> None:
        error: str
        for error in self._expected_errors:
            with self.subTest(error=error):
                self.assertIn(error, self._result.errors)
