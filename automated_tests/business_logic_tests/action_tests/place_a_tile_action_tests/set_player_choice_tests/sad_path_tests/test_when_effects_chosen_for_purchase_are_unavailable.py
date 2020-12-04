from typing import Dict, List, cast

from automated_tests.business_logic_tests.action_tests.place_a_tile_action_tests.given_a_place_a_tile_action import Given_A_PlaceATileAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests\
    .given_a_complete_dwarf_player_choice_transfer_service import FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from automated_tests.mocks.mock_card import MockCard
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect, AllowSubstitutionForPurchaseEffect, DecreasePriceOfTileEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_unknown_placement_lookup import TileUnknownPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_effects_chosen_for_purchase_are_unavailable(Given_A_PlaceATileAction):
    def because(self) -> None:
        self.initialise_sut_with_specific_tile()

        self._player: BasePlayerService = self.initialise_player()

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            [],
            1,
            2,
            HarvestTypeEnum.Harvest)

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice(
            self._player,
            self._dwarf_to_use,
            turn_descriptor
        )

        self._expected_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: 2,
            ResourceTypeEnum.ruby: 1,
        }

        self._action_invoked_result: ResultLookup[int] = self.SUT.invoke(
            self._player,
            None,  # Unused for this action
            self._dwarf_to_use  # Unused for this action
        )

    def initialise_player(self) -> BasePlayerService:
        self._dwarf_to_use: Dwarf = Dwarf(True)

        active_dwarf_1: Dwarf = Dwarf(True)
        active_dwarf_1.set_active(MockCard())

        active_dwarf_2: Dwarf = Dwarf(True)
        active_dwarf_2.set_active(MockCard())

        dwarves: List[Dwarf] = [active_dwarf_1, self._dwarf_to_use, active_dwarf_2]

        starting_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: 2,
            ResourceTypeEnum.ruby: 2,
        }

        # starting cost:      wood 4, stone 3
        # after substitution: wood 2, stone 0, ore 2
        # after decrease:     wood 2, stone 0, ore 0
        # final resources:    wood 0, stone 0, ore 0, ruby 2
        effects_to_use: Dict[BaseTilePurchaseEffect, int] = {
            DecreasePriceOfTileEffect(
                {
                    ResourceTypeEnum.ore: 2
                }): 1,
            AllowSubstitutionForPurchaseEffect(
                {
                    ResourceTypeEnum.stone: 3,
                    ResourceTypeEnum.wood: 2
                },
                {
                    ResourceTypeEnum.ore: 2
                }): 1,
        }

        player: MockPlayer = MockPlayer(dwarves, starting_resources)
        self._location_to_place_tile: int = 28
        player.get_player_choice_location_to_build_returns(
            lambda _, __, ___: ResultLookup(
                True,
                TileUnknownPlacementLookup(self._location_to_place_tile, None)
            ))
        player.get_player_choice_effects_to_use_for_cost_discount_returns(lambda _, __, ___: effects_to_use)
        return player

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_should_have_no_actions(self) -> None:
        self.assertEqual(len(self._result.value.actions), 0)

    def test_then_result_value_should_have_no_constraints(self) -> None:
        self.assertEqual(len(self._result.value.constraints), 0)

    def test_then_action_invoked_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoked_result)

    def test_then_action_invoked_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._action_invoked_result.flag)

    def test_then_action_invoked_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoked_result.value)

    def test_then_action_invoked_result_value_should_be_expected(self) -> None:
        self.assertEqual(0, self._action_invoked_result.value)

    def test_then_action_invoked_result_errors_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(List, self._action_invoked_result.errors)), 0)
