from typing import cast, Dict

from automated_tests.business_logic_tests.action_tests.breed_animals_action_tests.given_a_breed_animals_action import Given_A_BreedAnimalsAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests \
    .given_a_complete_dwarf_player_choice_transfer_service import FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_player_attempts_to_breed_more_animals_than_is_permitted(Given_A_BreedAnimalsAction):
    # noinspection PyTypeChecker
    def because(self) -> None:
        player: BasePlayerService = self._initialise_player()

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            [],
            0,
            0,
            HarvestTypeEnum.NoHarvest
        )

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice(
            player,
            None,
            turn_descriptor
        )

    def _initialise_player(self) -> MockPlayer:
        self._starting_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.sheep: 1,
            ResourceTypeEnum.donkey: 1,
            ResourceTypeEnum.cow: 2,
            ResourceTypeEnum.stone: 1
        }

        player: MockPlayer = MockPlayer(resources=self._starting_resources)

        player.get_player_choice_animals_to_breed_returns(
            lambda _, __, ___: ResultLookup(
                True,
                [ResourceTypeEnum.sheep, ResourceTypeEnum.donkey, ResourceTypeEnum.cow, ResourceTypeEnum.boar]))

        return player

    def test_then_invoke_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_invoke_flag_should_be_false(self) -> None:
        self.assertFalse(self._result.flag)

    def test_then_invoke_value_should_be_none(self) -> None:
        self.assertIsNone(self._result.value)

    def test_then_invoke_errors_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(list, self._result.errors)), 0)
