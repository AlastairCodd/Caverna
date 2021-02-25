from typing import List

from buisness_logic.services.turn_transfer_service import TurnTransferService, ChosenDwarfCardActionCombinationAndEquivalentLookup
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf_card_action_combination_lookup import DwarfCardActionCombinationLookup
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.action_invoke_service import ActionInvokeService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.services.base_player_service import BasePlayerService


class TurnExecutionService(object):
    def __init__(self) -> None:
        self._turn_transfer_service: TurnTransferService = TurnTransferService()
        self._action_invoke_service: ActionInvokeService = ActionInvokeService()

    def take_turn(
            self,
            player: BasePlayerService,
            turn_descriptor: TurnDescriptorLookup) -> None:
        if player is None:
            raise ValueError("Player cannot be None")
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor cannot be None")

        chosen_turn_descriptor_result: ResultLookup[ChosenDwarfCardActionCombinationAndEquivalentLookup] = self._turn_transfer_service.get_turn(
            player,
            turn_descriptor)

        success: bool = True
        errors: List[str] = []

        success &= chosen_turn_descriptor_result.flag
        errors.extend(chosen_turn_descriptor_result.errors)

        if chosen_turn_descriptor_result.flag:
            choice: DwarfCardActionCombinationLookup = chosen_turn_descriptor_result.value.choice

            actions_to_take: List[BaseAction] = choice.actions.actions
            constraints_on_actions: List[BaseConstraint] = choice.actions.constraints

            for action in actions_to_take:
                if isinstance(action, BasePlayerChoiceAction):
                    player_choice_result: ResultLookup[ActionChoiceLookup] = action.set_player_choice(
                        player,
                        choice.dwarf,
                        turn_descriptor)

                    success &= player_choice_result.flag
                    errors.extend(player_choice_result.errors)

                    if player_choice_result.flag:
                        actions_to_take.extend(player_choice_result.value.actions)
                        constraints_on_actions.extend(player_choice_result.value.constraints)

            if success:
                full_action_choice: ActionChoiceLookup = ActionChoiceLookup(actions_to_take, constraints_on_actions)

                invoked_result: ResultLookup[int] = self._action_invoke_service.invoke(
                    full_action_choice,
                    player,
                    choice.card,
                    choice.dwarf)

                success &= invoked_result.flag
                errors.extend(invoked_result.errors)

                if invoked_result.flag:
                    pass