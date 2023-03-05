from typing import List, Dict, cast

from automated_tests.common_tests.service_tests.exhaustive_action_ordering_service_tests.given_an_exhaustive_action_ordering_service import \
    Given_An_ExhaustiveActionOrderingService
from automated_tests.mocks.mock_card import MockCard
from automated_tests.mocks.mock_player import MockPlayer
from automated_tests.mocks.mock_tile import MockTile
from buisness_logic.actions.give_dwarf_a_weapon_action import GiveDwarfAWeaponAction
from buisness_logic.actions.go_on_an_expedition_action import GoOnAnExpeditionAction
from buisness_logic.actions.place_a_single_tile_action import PlaceASingleTileAction
from buisness_logic.actions.take_accumulated_items_action import TakeAccumulatedItemsAction
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.multiconditional import Conditional
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class test_when_called_with_single_highest_score_and_no_constraints(Given_An_ExhaustiveActionOrderingService):
    def because(self) -> None:
        action1_take_items: BaseAction = TakeAccumulatedItemsAction()
        action2_place_tile: BasePlayerChoiceAction = PlaceASingleTileAction()
        action3_get_weapon: BasePlayerChoiceAction = GiveDwarfAWeaponAction()
        action4_expedition: BasePlayerChoiceAction = GoOnAnExpeditionAction(level=2)

        actions: List[BaseAction] = [action1_take_items, action2_get_weapon, action3_expedition]
        constraints: List[BaseConstraint] = []
        action_choice_lookup: ActionChoiceLookup = ActionChoiceLookup(actions, constraints)

        self._expected_best_ordering: List[BaseAction] = [action1_take_items, action2_get_weapon, action3_expedition]

        resources: Dict[ResourceTypeEnum, int] = {}

        player: MockPlayer = MockPlayer(resources=resources)
        action_conditional: Conditional = Conditional(
            ActionCombinationEnum.AndOr,
            Conditional(
                ActionCombinationEnum.AndThen,
                action1_take_items,
                action2_place_tile),
            Conditional(
                ActionCombinationEnum.AndOr,
                action3_get_weapon,
                action4_expedition))
        current_card: BaseCard = MockCard(actions=action_conditional, resources={ResourceTypeEnum.ore: 3})
        current_dwarf: Dwarf = Dwarf()
        turn_descriptor

        turn_descriptor = self.initialise_actions(
            player,
            current_dwarf,
            actions)

        self._result: ResultLookup[List[BaseAction]] = self.SUT.calculate_best_order(
            action_choice_lookup,
            player,
            current_card,
            current_dwarf,
            turn_descriptor)

    def initialise_actions(
            self,
            player: MockPlayer,
            dwarf: Dwarf,
            actions: List[BaseAction]) -> TurnDescriptorLookup:

        player.get_player_choice_weapon_level_returns(lambda info_turn_descriptor: 3)

        player.get_player_choice_expedition_rewards_returns(
            lambda info_actions, info_expedition_level, info_turn_descriptor: ResultLookup(True, [info_actions[i] for i in range(info_expedition_level)])
        )

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [MockCard(), MockCard()],
            [MockTile()],
            0,
            0,
            HarvestTypeEnum.NoHarvest)

        for action in actions:
            if isinstance(action, BasePlayerChoiceAction):
                action.set_player_choice(
                    player,
                    dwarf,
                    turn_descriptor)

        return turn_descriptor

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_expected(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_be_in_expected_order(self) -> None:
        self.assertListEqual(self._result.value, self._expected_best_ordering)

    def test_then_result_errors_should_be_empty(self) -> None:
        self.assertListEqual(cast(list, self._result.errors), [])
