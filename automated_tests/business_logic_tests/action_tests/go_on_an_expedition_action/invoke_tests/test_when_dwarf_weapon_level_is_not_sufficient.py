from typing import List, cast

from automated_tests.business_logic_tests.action_tests.go_on_an_expedition_action.given_a_go_on_expedition_action import \
    Given_A_GoOnAnExpeditionAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests \
    .given_a_complete_dwarf_player_choice_transfer_service import FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.actions.upgrade_dwarf_weapon_action import UpgradeDwarfWeaponAction
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.entities.weapon import Weapon
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_dwarf_weapon_level_is_not_sufficient(Given_A_GoOnAnExpeditionAction):
    def because(self) -> None:
        player: BasePlayerService = self.initialise_player()

        dwarf: Dwarf = Dwarf(True)
        weapon: Weapon = Weapon(2)
        dwarf.give_weapon(weapon)

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            [],
            1,
            2,
            HarvestTypeEnum.Harvest)

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice(
            player,
            dwarf,
            turn_descriptor
        )

        self._action_invoke_result: ResultLookup[int] = self.SUT.invoke(
            player,
            FakeCard(),
            dwarf)

    def initialise_player(self) -> BasePlayerService:
        player: MockPlayer = MockPlayer()
        player.get_player_choice_expedition_rewards_returns(self._expedition_reward_func)
        return player

    def _expedition_reward_func(
            self,
            available_actions: List[BaseAction],
            level: int,
            unused_turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseAction]]:
        chosen_actions: List[BaseAction] = [available_actions[i] for i in range(-1, level - 1)]

        upgrade_weapon_action: BaseAction = UpgradeDwarfWeaponAction()

        self._expected_actions: List[BaseAction] = [upgrade_weapon_action]
        self._expected_actions.extend(chosen_actions)

        after_parent_constraints: List[BaseConstraint] = [PrecedesConstraint(self.SUT, action) for action in chosen_actions]
        before_upgrade_constraints: List[BaseConstraint] = [PrecedesConstraint(action, upgrade_weapon_action) for action in chosen_actions]

        self._expected_constraints: List[BaseConstraint] = [PrecedesConstraint(self.SUT, upgrade_weapon_action)]
        self._expected_constraints.extend(after_parent_constraints)
        self._expected_constraints.extend(before_upgrade_constraints)

        return ResultLookup(True, chosen_actions)

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_actions_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result.value.actions)

    def test_then_result_value_actions_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(List, self._result.value.actions)), 0)

    def test_then_result_value_actions_should_contain_expected_number_of_actions(self) -> None:
        self.assertEqual(len(cast(List, self._result.value.actions)), len(self._expected_actions))

    def test_then_result_value_actions_should_contain_expected_actions(self) -> None:
        for action in self._expected_actions:
            with self.subTest(actions=action):
                self.assertIn(action, self._result.value.actions)

    def test_then_result_value_constraints_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result.value.constraints)

    def test_then_result_value_constraints_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(List, self._result.value.constraints)), 0)

    def test_then_result_value_constraints_should_have_expected_number_of_constraints(self) -> None:
        self.assertEqual(len(cast(List, self._result.value.constraints)), len(self._expected_constraints))

    def test_then_result_value_constraints_should_contain_expected_constraint(self) -> None:
        for constraint in self._expected_constraints:
            with self.subTest(constraint=constraint):
                self.assertIn(constraint, self._result.value.constraints)

    def test_then_action_invoke_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoke_result)

    def test_then_action_invoke_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._action_invoke_result.flag)

    def test_then_action_invoke_result_value_should_be_none(self) -> None:
        self.assertIsNone(self._action_invoke_result.value)

    def test_then_action_invoke_result_errors_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(list, self._action_invoke_result.errors)), 0)
