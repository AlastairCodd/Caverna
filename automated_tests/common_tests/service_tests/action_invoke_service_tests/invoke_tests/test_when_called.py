from typing import List, cast, Optional, Dict

from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.given_a_turn_execution_service import FakeCard
from automated_tests.common_tests.service_tests.action_invoke_service_tests.given_an_action_invoke_service import Given_An_ActionInvokeService
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.actions.activate_dwarf_action import ActivateDwarfAction
from buisness_logic.actions.place_a_twin_tile_action import PlaceATwinTileAction
from buisness_logic.actions.take_accumulated_items_action import TakeAccumulatedItemsAction
from buisness_logic.cards.drift_mining_card import DriftMiningTwoStoneCard
from buisness_logic.tiles.mine_tiles import CavernTile, TunnelTile
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.tile_unknown_placement_lookup import TileUnknownPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum, TileDirectionEnum, ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class test_when_called(Given_An_ActionInvokeService):
    def because(self) -> None:
        activate_dwarf_action: BaseAction = ActivateDwarfAction()
        take_accumulated_items_action: BaseAction = TakeAccumulatedItemsAction()
        place_a_twin_tile_action: BasePlayerChoiceAction = PlaceATwinTileAction(TileTypeEnum.cavernTunnelTwin)

        actions: List[BaseAction] = [
            activate_dwarf_action,
            take_accumulated_items_action,
            place_a_twin_tile_action]

        constraints: List[BaseConstraint] = [
            PrecedesConstraint(take_accumulated_items_action, place_a_twin_tile_action),
            PrecedesConstraint(activate_dwarf_action, take_accumulated_items_action),
            PrecedesConstraint(activate_dwarf_action, place_a_twin_tile_action),
        ]

        action_choice: ActionChoiceLookup = ActionChoiceLookup(
            actions,
            constraints)

        self._dwarf: Dwarf = Dwarf(is_adult=True)
        self._player: BasePlayerRepository = self._initialise_player(place_a_twin_tile_action, self._dwarf)

        self._card: BaseResourceContainingCard = DriftMiningTwoStoneCard()
        self._card.refill_action()

        self._result: ResultLookup[int] = self.SUT.invoke(
            action_choice,
            self._player,
            self._card,
            self._dwarf)

        self._expected_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.stone: 2,
        }

    def _initialise_player(
            self,
            action: BasePlayerChoiceAction,
            dwarf: Dwarf) -> BasePlayerRepository:
        player: MockPlayer = MockPlayer()
        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup([FakeCard()], [], 0, 0, HarvestTypeEnum.Harvest)

        #          |  u  u  u                   |  4  5  6
        #  _  _  _ |  u  u  u  u        _  _  _ | 12 13 14 15
        #  _  _  _ |  u  u  u  u        _  _  _ | 20 21 22 23
        #  _  _  _ |  c  u  u  u        _  _  _ | 28 29 30 31
        #  _  _  _ | En  u  u  u        _  _  _ | 36 37 38 39
        #          |  u  u  u                   | 44 45 46

        location_to_place_primary_tile: int = 37
        location_to_place_secondary_tile: int = 29

        player.get_player_choice_location_to_build_returns(
            lambda _, __, ___: ResultLookup(True, TileUnknownPlacementLookup(location_to_place_primary_tile, TileDirectionEnum.up))
        )

        self._expected_tiles: Dict[int, BaseTile] = {
            location_to_place_primary_tile: CavernTile(),
            location_to_place_secondary_tile: TunnelTile(),
        }

        action.set_player_choice(player, dwarf, turn_descriptor)

        return player

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_should_be_expected(self) -> None:
        self.assertEqual(self._result.value, 5)

    def test_then_result_errors_should_be_empty(self) -> None:
        self.assertListEqual(cast(list, self._result.errors), [])

    def test_then_player_should_have_tiles_at_expected_locations(self) -> None:
        for tile_location in self._expected_tiles:
            with self.subTest(location=tile_location):
                expected_tile: Optional[BaseTile] = self._expected_tiles[tile_location]
                if expected_tile is not None:
                    self.assertIs(self._player.tiles[tile_location].tile.id, expected_tile.id)
                else:
                    self.assertIsNone(self._player.tiles[tile_location].tile)

    def test_then_player_should_have_expected_amount_of_resources(self) -> None:
        for resource in self._expected_resources:
            with self.subTest(resource=resource):
                expected_amount: int = self._expected_resources[resource]
                if expected_amount == 0:
                    self.assertNotIn(resource, self._player.resources)
                else:
                    self.assertEqual(self._player.resources[resource], expected_amount)