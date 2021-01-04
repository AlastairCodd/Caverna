from typing import Dict, cast

from automated_tests.business_logic_tests.action_tests.breed_animals_action_tests.given_a_breed_animals_action import Given_A_BreedAnimalsAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests \
    .given_a_complete_dwarf_player_choice_transfer_service import FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.tiles.mine_tiles import OreMineTile, RubyMineTile
from buisness_logic.tiles.outdoor_tiles import PastureTile
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.result_lookup import ResultLookup
from common.entities.tile_entity import TileEntity
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_player_has_sufficient_room_for_animals(Given_A_BreedAnimalsAction):
    # noinspection PyTypeChecker
    def because(self) -> None:
        self._player: BasePlayerService = self._initialise_player()

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            [],
            0,
            0,
            HarvestTypeEnum.Harvest)

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice(
            self._player,
            None,  # Unused
            turn_descriptor)

        self._action_invoke_result: ResultLookup[int] = self.SUT.invoke(
            self._player,
            None,  # Unused
            None)  # Unused

        self._expected_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.sheep: 3,
            ResourceTypeEnum.donkey: 3,
            ResourceTypeEnum.cow: 2,
            ResourceTypeEnum.stone: 1
        }

    def _initialise_player(self) -> MockPlayer:
        starting_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.sheep: 2,
            ResourceTypeEnum.donkey: 2,
            ResourceTypeEnum.cow: 2,
            ResourceTypeEnum.stone: 1
        }

        player: MockPlayer = MockPlayer(resources=starting_resources)

        # _ 1 2 _ | _ _ _ 7
        # 8 x x x | x x x _
        # _ x x x | x x x _
        # _ x x x | C x x _
        # _ x x P | D m m dm
        # _ _ _ _ | _ _ _ _

        outside_pasture_tile_entity: TileEntity = player.tiles[35]
        outside_pasture_tile_entity.set_tile(PastureTile())
        outside_pasture_tile_entity.give_stable()

        player.tiles[37].set_tile(OreMineTile())
        player.tiles[38].set_tile(OreMineTile())
        player.tiles[39].set_tile(RubyMineTile())

        self._animals_to_breed = [ResourceTypeEnum.sheep, ResourceTypeEnum.donkey]
        player.get_player_choice_animals_to_breed_returns(
            lambda _, __, ___: ResultLookup(
                True,
                self._animals_to_breed))

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

    def test_then_result_errors_should_be_empty(self) -> None:
        self.assertListEqual([], cast(list, self._result.errors))

    def test_then_action_invoke_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoke_result)

    def test_then_action_invoke_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._action_invoke_result.flag)

    def test_then_action_invoke_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoke_result.value)

    def test_then_action_invoke_result_value_should_be_expected(self) -> None:
        self.assertEqual(self._action_invoke_result.value, len(self._animals_to_breed))

    def test_then_action_invoke_result_errors_should_be_empty(self) -> None:
        self.assertListEqual([], cast(list, self._action_invoke_result.errors))

    def test_then_player_should_have_expected_amount_of_resources(self) -> None:
        for resource in self._expected_resources:
            with self.subTest(resource=resource):
                expected_amount: int = self._expected_resources[resource]
                if expected_amount == 0:
                    self.assertNotIn(resource, self._player.resources)
                else:
                    self.assertEqual(self._player.resources[resource], expected_amount)
