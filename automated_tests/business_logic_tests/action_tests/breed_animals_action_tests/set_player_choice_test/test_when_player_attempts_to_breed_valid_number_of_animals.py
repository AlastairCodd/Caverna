from typing import cast, Dict

from automated_tests.business_logic_tests.action_tests.breed_animals_action_tests.given_a_breed_animals_action import Given_A_BreedAnimalsAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests \
    .given_a_complete_dwarf_player_choice_transfer_service import FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.actions.check_animal_storage_action import CheckAnimalStorageAction
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_player_attempts_to_breed_valid_number_of_animals(Given_A_BreedAnimalsAction):
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
                [ResourceTypeEnum.sheep, ResourceTypeEnum.donkey, ResourceTypeEnum.cow]))

        return player

    def test_then_invoke_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_invoke_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_invoke_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_actions_should_contain_expected_actions(self) -> None:
        self.assertIn(CheckAnimalStorageAction(), self._result.value.actions)

    def test_then_result_value_should_have_expected_number_of_constraints(self) -> None:
        self.assertEqual(len(self._result.value.constraints), 1)

    def test_then_result_value_constraints_should_contain_expected_constraints(self) -> None:
        self.assertIn(PrecedesConstraint(self.SUT, CheckAnimalStorageAction()), self._result.value.constraints)

    def test_then_invoke_errors_should_be_empty(self) -> None:
        self.assertListEqual(cast(list, self._result.errors), [])
