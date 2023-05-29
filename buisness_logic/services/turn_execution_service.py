from typing import List, Optional, Any
import logging

from buisness_logic.actions.check_animal_storage_action import CheckAnimalStorageAction
from buisness_logic.actions.convert_action import ConvertAction
from buisness_logic.actions.resolve_harvest_action import ResolveHarvestAction
from buisness_logic.services.turn_transfer_service import TurnTransferService, ChosenDwarfCardActionCombinationAndEquivalentLookup
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.dwarf_card_action_combination_lookup import DwarfCardActionCombinationLookup
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.action_invoke_service import ActionInvokeService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_action_ordering_service import ActionOrderingService
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.services.base_player_service import BasePlayerService


class TurnExecutionService(object):
    def __init__(self, action_ordering_service: Optional[ActionOrderingService] = None) -> None:
        self._turn_transfer_service: TurnTransferService = TurnTransferService()
        self._action_invoke_service: ActionInvokeService = ActionInvokeService(action_ordering_service)

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

        logging.debug(chosen_turn_descriptor_result.value.choice.__format__("4"))

        choice: DwarfCardActionCombinationLookup = chosen_turn_descriptor_result.value.choice

        untested_actions: List[BaseAction] = []
        untested_actions.extend(choice.actions.actions)
        untested_actions.append(ConvertAction())

        has_check_for_animal_storage = False
        actions_to_take: List[BaseAction] = []
        constraints_on_actions: List[BaseConstraint] = []

        constraints_on_actions.extend(choice.actions.constraints)

        action: BaseAction
        for action in untested_actions:
            if isinstance(action, CheckAnimalStorageAction):
                if not has_check_for_animal_storage:
                    has_check_for_animal_storage = True
                    actions_to_take.append(action)
                continue
            if not isinstance(action, BasePlayerChoiceAction):
                actions_to_take.append(action)
                continue

            handle_result = self._handle_action(
                action,
                player,
                choice.dwarf,
                turn_descriptor,
                actions_to_take,
                constraints_on_actions,
                untested_actions)

            success &= handle_result.flag
            errors.extend(handle_result.errors)

        if not success:
            return ResultLookup(errors=errors)

        if is_players_final_turn:
            harvest_result = self._handle_harvest(
                action,
                player,
                choice.dwarf,
                turn_descriptor,
                actions_to_take,
                constraints_on_actions,
                has_check_for_animal_storage)

            errors.extend(harvest_result.errors)

            if not harvest_result.flag:
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

    def _handle_action(
            self,
            action: BaseAction,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup,
            actions_to_take: List[BaseAction],
            constraints_on_actions: List[BaseConstraint],
            untested_actions: List[BaseAction]) -> ResultLookup[Any]:
        set_result: ResultLookup[ActionChoiceLookup] = action.set_player_choice(
            player,
            dwarf,
            turn_descriptor)

        if not set_result.flag:
            return set_result
        constraints_on_actions.extend(set_result.value.constraints)
        actions_to_take.append(action)

        self._constrain_children_of_action_to_happen_after_action(
            action,
            set_result.value.actions,
            untested_actions,
            constraints_on_actions)

        return set_result

    def _handle_harvest(
            self,
            action: BaseAction,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup,
            actions_to_take: List[BaseAction],
            constraints_on_actions: List[BaseConstraint],
            has_check_for_animal_storage: bool) -> ResultLookup[Any]:
        harvest_action: BaseAction = ResolveHarvestAction()

        set_result = harvest_action.set_player_choice(
            player,
            dwarf,
            turn_descriptor)

        if not set_result.flag:
            return ResultLookup(errors=set_result.errors)

        # enforce that harvest happens after other actions
        for action in actions_to_take:
            # don't require that harvest must happen after check animal, bcs sometimes we get more animals during harvest
            if isinstance(action, CheckAnimalStorageAction):
                continue
            constraints_on_actions.append(PrecedesConstraint(action, harvest_action))
        actions_to_take.append(harvest_action)

        success = True
        errors = []
        untested_actions = []

        self._constrain_children_of_action_to_happen_after_action(
            harvest_action,
            set_result.value.actions,
            untested_actions,
            constraints_on_actions)

        constraints_on_actions.extend(set_result.value.constraints)

        for action in untested_actions:
            if isinstance(action, CheckAnimalStorageAction):
                if not has_check_for_animal_storage:
                    has_check_for_animal_storage = True
                    actions_to_take.append(action)
                continue
            if not isinstance(action, BasePlayerChoiceAction):
                actions_to_take.append(action)
                continue

            handle_result = self._handle_action(
                action,
                player,
                dwarf,
                turn_descriptor,
                actions_to_take,
                constraints_on_actions,
                untested_actions)

            success &= handle_result.flag
            errors.extend(handle_result.errors)

        return ResultLookup(True, None, errors)

    def _constrain_children_of_action_to_happen_after_action(
            self,
            parent_action: BaseAction,
            child_actions: list[BaseAction],
            untested_actions: list[BaseAction],
            constraints_on_actions: list[BaseConstraint]) -> None:
        child_action: BaseAction
        for child_action in child_actions:
            untested_actions.append(child_action)
            if isinstance(child_action, CheckAnimalStorageAction):
                # the constraint that "check animal storage" happens after "receive animal" is enforced
                #    in the action themselves -- no point duplicating the constraint here
                #    (there wouldn't be any side effects, its just messy)
                continue
            new_constraint: BaseConstraint = PrecedesConstraint(parent_action, child_action)
            constraints_on_actions.append(new_constraint)
