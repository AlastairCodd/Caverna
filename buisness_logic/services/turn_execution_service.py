from typing import List

from buisness_logic.actions.resolve_harvest_action import ResolveHarvestAction
from buisness_logic.services.turn_transfer_service import TurnTransferService, ChosenDwarfCardActionCombinationAndEquivalentLookup
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf_card_action_combination_lookup import DwarfCardActionCombinationLookup
from common.entities.precedes_constraint import PrecedesConstraint
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
            is_players_final_turn: bool,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player cannot be None")
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor cannot be None")

        chosen_turn_descriptor_result: ResultLookup[ChosenDwarfCardActionCombinationAndEquivalentLookup] = self._turn_transfer_service.get_turn(
            player,
            turn_descriptor)

        if not chosen_turn_descriptor_result.flag:
            return ResultLookup(errors=chosen_turn_descriptor_result.errors)

        success: bool = True
        errors: List[str] = []
        count: int = 0

        success &= chosen_turn_descriptor_result.flag
        errors.extend(chosen_turn_descriptor_result.errors)

        print(f"[VRB] {chosen_turn_descriptor_result.value.choice:4}")

        choice: DwarfCardActionCombinationLookup = chosen_turn_descriptor_result.value.choice

        untested_actions: List[BaseAction] = []
        untested_actions.extend(choice.actions.actions)

        if is_players_final_turn:
            harvest_action: BaseAction = ResolveHarvestAction()
            untested_actions.append(harvest_action)

        actions_to_take: List[BaseAction] = []
        constraints_on_actions: List[BaseConstraint] = []

        constraints_on_actions.extend(choice.actions.constraints)

        action: BaseAction
        for action in untested_actions:
            if not isinstance(action, BasePlayerChoiceAction):
                actions_to_take.append(action)
                continue
            set_result: ResultLookup[ActionChoiceLookup] = action.set_player_choice(
                player,
                choice.dwarf,
                turn_descriptor)

            success &= set_result.flag
            errors.extend(set_result.errors)

            if not set_result.flag:
                continue
            constraints_on_actions.extend(set_result.value.constraints)
            actions_to_take.append(action)

            new_action: BaseAction
            for new_action in set_result.value.actions:
                untested_actions.append(new_action)
                new_constraint: BaseConstraint = PrecedesConstraint(action, new_action)
                constraints_on_actions.append(new_constraint)

        if not success:
            return ResultLookup(errors=errors)

        full_action_choice: ActionChoiceLookup = ActionChoiceLookup(actions_to_take, constraints_on_actions)

        invoked_result: ResultLookup[int] = self._action_invoke_service.invoke(
            full_action_choice,
            player,
            choice.card,
            choice.dwarf,
            turn_descriptor)

        success &= invoked_result.flag
        errors.extend(invoked_result.errors)

        if invoked_result.flag:
            count = invoked_result.value

        return ResultLookup(success, count, errors)
