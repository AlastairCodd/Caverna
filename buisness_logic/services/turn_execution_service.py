from typing import List, Optional, Any, Tuple
from abc import abstractmethod, ABCMeta
from enum import Enum, auto
import logging

from buisness_logic.actions.check_animal_storage_action import CheckAnimalStorageAction
from buisness_logic.actions.convert_action import ConvertAction
from buisness_logic.actions.free_action import FreeAction
from buisness_logic.actions.resolve_harvest_action import ResolveHarvestAction
from buisness_logic.services.complete_action_player_choice_transfer_service import CompleteActionPlayerChoiceTransferService
from buisness_logic.services.complete_card_player_choice_transfer_service import CompleteCardPlayerChoiceTransferService
from buisness_logic.services.complete_dwarf_player_choice_transfer_service import CompleteDwarfPlayerChoiceTransferService
from buisness_logic.services.turn_transfer_service import TurnTransferService, ChosenDwarfCardActionCombinationAndEquivalentLookup
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.dwarf_card_action_combination_lookup import DwarfCardActionCombinationLookup
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.configurable_action_ordering_service import ConfigurableActionOrderingService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_action_ordering_service import ActionOrderingService
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.constants.logging import VERBOSE_LOG_LEVEL, DollarMessage as __
from core.services.base_player_service import BasePlayerService


class TurnExecutionService(object):
    def __init__(self, action_ordering_service: Optional[ActionOrderingService] = None) -> None:
        self._turn_transfer_service: TurnTransferService = TurnTransferService()
        self._action_ordering_service: ActionOrderingService = action_ordering_service if action_ordering_service is not None else ConfigurableActionOrderingService()

    def take_turn(
            self,
            player: BasePlayerService,
            is_players_final_turn: bool,
            turn_descriptor: TurnDescriptorLookup):
        if player is None:
            raise ValueError("Player cannot be None")
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor cannot be None")

        turn_state = ChooseDwarfTurnState(player, is_players_final_turn, turn_descriptor)
        while turn_state is not None:
            turn_state = turn_state.next()

    def _constrain_children_of_action_to_happen_after_action(
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

class TurnState(metaclass=ABCMeta):
    @abstractmethod
    def next(self) -> 'TurnState':
        pass

class ChooseDwarfTurnState(TurnState):
    def __init__(self, player, is_players_final_turn, turn_descriptor) -> None:
        self._player = player
        self._is_players_final_turn = is_players_final_turn
        self._turn_descriptor = turn_descriptor
        self._dwarf_transfer_service = CompleteDwarfPlayerChoiceTransferService()

    def next(self) -> TurnState:
        dwarf_result = self._dwarf_transfer_service.get_dwarf(
                self._player,
                self._turn_descriptor)
        
        if not dwarf_result.flag:
            warnings.warn("inform player of incorrect dwarf choice")
            return self

        chosen_dwarf, dwarf_action_choice = dwarf_result.value
        return ChooseCardTurnState(
                self._player,
                self._is_players_final_turn,
                chosen_dwarf,
                dwarf_action_choice,
                self._turn_descriptor)

class ChooseCardTurnState(TurnState):
    def __init__(
            self,
            player,
            is_players_final_turn,
            dwarf,
            dwarf_actions,
            turn_descriptor) -> None:
        self._player = player
        self._is_players_final_turn = is_players_final_turn
        self._dwarf = dwarf
        self._dwarf_actions = dwarf_actions
        self._turn_descriptor = turn_descriptor
        self._card_transfer_service = CompleteCardPlayerChoiceTransferService()

    def next(self) -> TurnState:
        card_result = self._card_transfer_service.get_card(
                self._player,
                self._dwarf,
                self._turn_descriptor)

        if not card_result.flag:
            warnings.warn("inform player of incorrect card choice and let them decide to choose different dwarf")
            return self

        chosen_card, card_action_choice = card_result.value
        return ChooseActionsTurnState(
                self._player,
                self._is_players_final_turn,
                self._dwarf,
                self._dwarf_actions,
                chosen_card, 
                card_action_choice,
                self._turn_descriptor)

class ChooseActionsTurnState(TurnState):
    def __init__(
            self,
            player,
            is_players_final_turn,
            dwarf,
            dwarf_actions,
            card,
            card_actions,
            turn_descriptor) -> None:
        self._player = player
        self._is_players_final_turn = is_players_final_turn
        self._dwarf = dwarf
        self._dwarf_actions = dwarf_actions
        self._card = card
        self._card_actions = card_actions
        self._turn_descriptor = turn_descriptor
        self._action_transfer_service = CompleteActionPlayerChoiceTransferService()

    def next(self) -> TurnState:
        action_result = self._action_transfer_service.get_action(
                self._player,
                self._dwarf,
                self._card,
                self._turn_descriptor)

        if not action_result.flag:
            warnings.warn("inform player of incorrect action combination")
            return self

        dwarf_action_choice = self._dwarf_actions
        card_action_choice = self._card_actions
        action_action_choice = action_result.value

        actions: List[BaseAction] = []
        actions.extend(dwarf_action_choice.actions)
        actions.extend(card_action_choice.actions)
        actions.extend(action_action_choice.actions)

        constraints: List[BaseConstraint] = []
        constraints.extend(dwarf_action_choice.constraints)
        constraints.extend(card_action_choice.constraints)
        constraints.extend(action_action_choice.constraints)

        for dwarf_action in dwarf_action_choice.actions:
            for card_action in card_action_choice.actions:
                constraint: BaseConstraint = PrecedesConstraint(dwarf_action, card_action)
                constraints.append(constraint)

            for action_action in action_action_choice.actions:
                constraint: BaseConstraint = PrecedesConstraint(dwarf_action, action_action)
                constraints.append(constraint)

        for card_action in card_action_choice.actions:
            for action_action in action_action_choice.actions:
                constraint: BaseConstraint = PrecedesConstraint(card_action, action_action)
                constraints.append(constraint)

        action_tree = ActionTree(actions, constraints, self._is_players_final_turn)

        return MakeChoicesForActionsTurnState(
                self._player,
                self._dwarf,
                self._card,
                action_tree,
                self._turn_descriptor)

class VisitResult(Enum):
    set_successfully = auto()
    failed = auto()
    none_remaining = auto()

class ActionTree(object):
    def __init__(self, actions, constraints, is_players_final_turn) -> None:
        self._untested_actions = actions
        self._untested_actions.append(ConvertAction())
        self._untested_actions.append(FreeAction())

        self._actions_to_take = []
        self._constraints = constraints
        self._has_check_for_animal_storage = False
        self._is_players_final_turn = is_players_final_turn

    def get_next_action(self) -> BaseAction:
        while len(self._untested_actions) > 0:
            action = self._untested_actions.pop(0)
            if not isinstance(action, CheckAnimalStorageAction):
                return action
            if not self._has_check_for_animal_storage:
                self._has_check_for_animal_storage = True
                return action

        return None

    def visit(self, player, dwarf, turn_descriptor) -> VisitResult | Tuple[VisitResult, ActionChoiceLookup] | Tuple[VisitResult, BaseAction, list[str]]:
        next_action = self.get_next_action()
        if next_action is None:
            logging.log(VERBOSE_LOG_LEVEL, __("visited all actions"))
            if not self._is_players_final_turn:
                return (VisitResult.none_remaining, ActionChoiceLookup(self._actions_to_take, self._constraints))
            logging.log(VERBOSE_LOG_LEVEL, __("... but is palyers final turn, so adding harvest action"))
            next_action = self._resolve_harvest()
        logging.log(VERBOSE_LOG_LEVEL, __("visiting {action!r}", action=next_action))
        if not isinstance(next_action, BasePlayerChoiceAction):
            self._actions_to_take.append(next_action)
            return VisitResult.set_successfully

        result = next_action.set_player_choice(player, dwarf, turn_descriptor)
        if not result.flag:
            return (VisitResult.failure, action, result.errors)

        self._constraints.extend(result.value.constraints)
        self._actions_to_take.append(next_action)

        TurnExecutionService._constrain_children_of_action_to_happen_after_action(
                next_action,
                result.value.actions,
                self._untested_actions,
                self._constraints)

        return VisitResult.set_successfully

    def _resolve_harvest(self) -> BaseAction:
        harvest_action = ResolveHarvestAction()

        # enforce that harvest happens after other actions
        for action in self._actions_to_take:
            # don't require that harvest must happen after check animal, bcs sometimes we get more animals during harvest
            if isinstance(action, CheckAnimalStorageAction):
                continue
            self._constraints.append(PrecedesConstraint(action, harvest_action))
        
        self._is_players_final_turn = False
        return harvest_action

class MakeChoicesForActionsTurnState(TurnState):
    def __init__(
            self,
            player,
            dwarf,
            card,
            action_tree,
            turn_descriptor) -> None:
        self._player = player
        self._dwarf = dwarf
        self._card = card
        self._action_tree = action_tree
        self._turn_descriptor = turn_descriptor

    def next(self) -> TurnState:
        logging.log(VERBOSE_LOG_LEVEL, "starting to visit actions")
        while True:
            match self._action_tree.visit(
                    self._player,
                    self._dwarf,
                    self._turn_descriptor):
                case (VisitResult.none_remaining, full_action_choice):
                    return OrderActionsTurnState(
                            self._player,
                            self._dwarf,
                            self._card,
                            full_action_choice,
                            self._turn_descriptor)
                case VisitResult.set_successfully:
                    continue
                case (VisitResult.Failed, action, errors):
                    match self._player.report_action_choice_failed(action_result.value):
                        case InvalidActionCombinationResponse.ResetEntireChoice | InvalidActionCombinationResponse.UseDifferentDwarf:
                            return ChooseDwarfTurnState(self._player, self._turn_descriptor)
                        case InvalidActionCombinationResponse.PickCardAgain:
                            return ChooseCardTurnState(self._player, self._dwarf, self._turn_descriptor)
                        case InvalidActionCombinationResponse.MakeDifferentCardChoice:
                            return ChooseActionTurnState(self._player, self._dwarf, self._card, self._turn_descriptor)
                        case _:
                            raise NotImplementedError()
                case err:
                    raise ValueError(f"unknown enum or additional arguments: {err!r}")

class OrderActionsTurnState(TurnState):
    def __init__(
            self,
            player,
            dwarf,
            card,
            full_action_choice,
            turn_descriptor):
        self._player = player
        self._dwarf = dwarf
        self._card = card
        self._full_action_choice = full_action_choice
        self._turn_descriptor = turn_descriptor
        self._action_ordering_service = ConfigurableActionOrderingService()

    def next(self) -> TurnState:
        actions_best_order: ResultLookup[List[BaseAction]] = self._action_ordering_service.calculate_best_order(
            self._full_action_choice,
            self._player,
            self._card,
            self._dwarf,
            self._turn_descriptor)

        if not actions_best_order.flag:
            player_response = self._player.report_action_choice_failed(self._full_action_choice)
            raise NotImplementedError("TODO react to player choice")

        return InvokeBestOrderingTurnState(
                self._player,
                self._dwarf,
                self._card,
                actions_best_order.value)

class InvokeBestOrderingTurnState(TurnState):
    def __init__(
            self,
            player,
            dwarf,
            card,
            ordered_actions):
        self._player = player
        self._dwarf = dwarf
        self._card = card
        self._ordered_actions = ordered_actions

    def next(self) -> TurnState:
        logging.info("> returned valid ordering")

        for action in self._ordered_actions:
            logging.info(__("  > Invoking {action}", action=action))

            invoke_result: ResultLookup[int] = action.invoke(
                    self._player,
                    self._card,
                    self._dwarf)

            if not invoke_result.flag:
                raise InvalidOperationError("Ordering service's supposedly valid ordering was actually invalid")
            logging.debug(__("    > Success, {successes} actions", successes=invoke_result.value))

        return None
