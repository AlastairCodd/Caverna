from functools import reduce
from typing import List, Iterable, Tuple, Union, Optional, Callable

from buisness_logic.actions.activate_dwarf_action import ActivateDwarfAction
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.prototypes.player_prototype import PlayerPrototype
from common.prototypes.card_prototype import CardPrototype
from common.prototypes.dwarf_prototype import DwarfPrototype
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_action_ordering_service import ActionOrderingService
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_prototype import BaseImmutablePrototype
from core.baseClasses.base_permutation_ordering_service import BasePermutationOrderingService
from core.baseClasses.base_tile import BaseTile
from core.forges.base_list_permutation_forge import BaseListPermutationForge
from core.services.base_constraint_validator import BaseConstraintValidator
from core.exceptions.invalid_operation_error import InvalidOperationError
from core.repositories.base_player_repository import BasePlayerRepository


class ConfigurableActionOrderingService(ActionOrderingService):
    def __init__(
            self,
            permutation_ordering_services: Union[List[BasePermutationOrderingService], BasePermutationOrderingService, None] = None,
            permutation_forge: Optional[BaseListPermutationForge] = None,
            constraint_validator_func: Optional[Callable[List[BaseConstraint], BaseConstraintValidator]] = None):
        self._player_prototype: BaseImmutablePrototype[BasePlayerRepository] = PlayerPrototype()
        self._card_prototype: BaseImmutablePrototype[BaseCard] = CardPrototype()
        self._dwarf_prototype: BaseImmutablePrototype[Dwarf] = DwarfPrototype()

        self._permutation_forge: BaseListPermutationForge
        if permutation_forge is None:
            from common.forges.pruning_list_permutation_forge import PruningListPermutationForge
            self._permutation_forge = PruningListPermutationForge()
        else:
            self._permutation_forge = permutation_forge

        self._permutation_ordering_services: List[BasePermutationOrderingService]
        if permutation_ordering_services is None:
            from buisness_logic.services.most_points_permutation_ordering_service import MostPointsPermutationOrderingService
            from buisness_logic.services.most_resources_permutation_ordering_service import MostResourcesPermutationOrderingService
            self._permutation_ordering_services = [
                MostPointsPermutationOrderingService(),
                MostResourcesPermutationOrderingService()]
        else:
            if isinstance(permutation_ordering_services, list):
                self._permutation_ordering_services = list(permutation_ordering_services)
            else:
                self._permutation_ordering_services = [permutation_ordering_services]

        self._constraint_validator_func: Callable[List[BaseConstraint], BaseConstraintValidator]
        if constraint_validator_func is None:
            from common.services.collating_constraint_validator import CollatingConstraintValidator
            self._constraint_validator_func = lambda constraints: CollatingConstraintValidator(constraints)
        else:
            self._constraint_validator_func = constraint_validator_func

        self._turn_descriptor_tiles: Optional[List[BaseTile]] = None
        self._debug_flag_do_not_invoke_actions: bool = False

    def calculate_best_order(
            self,
            actions: ActionChoiceLookup,
            player: BasePlayerRepository,
            current_card: BaseCard,
            current_dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseAction]]:
        if actions is None:
            raise ValueError
        if player is None:
            raise ValueError
        if current_card is None:
            raise ValueError
        if current_dwarf is None:
            raise ValueError

        print(f"[DBG] ordering {len(actions.actions)} actions")
        for action in actions.actions:
            print(f"[VRB]   {action!r}")
        print(f"[DBG] with {len(actions.constraints)} constraints")
        for constraint in actions.constraints:
            print(f"[VRB]   {constraint!r}")

        successful_permutations: List[Tuple[List[BaseAction], int, BasePlayerRepository]] = []
        unsuccessful_permutations: List[ResultLookup[int]] = []

        permutation: List[BaseAction]
        permutations: Iterable[List[BaseAction]] = self._permutation_forge.generate_list_permutations(actions.actions)

        self._cache_turn_descriptor_state(turn_descriptor)
        permutation_index: int = 0

        constraint_validator = self._constraint_validator_func(actions.constraints)

        activate_dwarf_action: ActivateDwarfAction = [action for action in actions.actions if isinstance(action, ActivateDwarfAction)][0]

        for permutation in permutations:
            if not self._does_pass_all_constraints(permutation, constraint_validator):
                #print(f"permutation {permutation_index} does not pass constraints")
                permutation_index += 1
                continue
            if self._debug_flag_do_not_invoke_actions:
                permutation_index += 1
                continue

            # The cloned player for testing shouldn't need to make any decisions
            player_copy: BasePlayerRepository = self._player_prototype.clone(player)
            card_copy: BaseCard = self._card_prototype.clone(current_card)
            dwarf_copy: Dwarf = self._dwarf_prototype.clone(current_dwarf)

            self._reset_turn_descriptor(turn_descriptor)

            success: bool = True
            successes: int = 0
            errors_for_permutation: List[str] = []

            #print(f"[DBG] considering permutation {permutation_index}")

            action: BaseAction
            for (i, action) in enumerate(permutation):
                if not success: 
                    #print(f"[DBG]        _: action {i}: {action:4}")
                    continue
                action_result: ResultLookup[int]
                if action is activate_dwarf_action:
                    #print(f"[DBG]  success: action {i} {action:4}")
                    successes += 1
                    continue

                action_result = action.invoke(player_copy, card_copy, dwarf_copy)

                errors_for_permutation.extend(action_result.errors)

                if not action_result.flag:
                    #print(f"[DBG] *** FAIL: action {i} {action:4}")
                    success = False
                    self._permutation_forge.mark_last_permutation_as_invalid(i)
                    break

                #print(f"[DBG]  success: action {i} {action:4}")
                successes += action_result.value

            if success:
                success_result: Tuple[List[BaseAction], int, BasePlayerRepository] = (permutation, successes, player_copy)
                successful_permutations.append(success_result)
            else:
                permutation_result: ResultLookup[int] = ResultLookup(success, successes, errors_for_permutation)
                unsuccessful_permutations.append(permutation_result)
            #print("[VRB]")
            permutation_index += 1

        self.reset(turn_descriptor)

        permutation_ordering_service: BasePermutationOrderingService
        ranked_results: List[Tuple[List[BaseAction], int, BasePlayerRepository]] = successful_permutations

        number_of_successful_permutations = len(successful_permutations)
        number_of_unsuccessful_permutations = len(unsuccessful_permutations)
        total_permutations_that_passed_constraints = number_of_successful_permutations + number_of_unsuccessful_permutations 
        print(f"[INF] permutations considered: {total_permutations_that_passed_constraints}/{permutation_index} passed the constraint check, {number_of_successful_permutations}/{total_permutations_that_passed_constraints} are possible")
        if not any(successful_permutations):
            errors: List[str] = ["There is not a permutation which allows for all actions to be performed"]
            for partition in unsuccessful_permutations:
                errors.extend(partition.errors)
            errors = list(set(errors))
            return ResultLookup(errors=errors)

        permutation_ordering_service: BasePermutationOrderingService
        ranked_results: List[Tuple[List[BaseAction], int, BasePlayerRepository]] = successful_permutations

        for permutation_ordering_service in self._permutation_ordering_services:
            ordering_result: ResultLookup[List[Tuple[List[BaseAction], int, BasePlayerRepository]]] = permutation_ordering_service \
                .find_best_permutation(ranked_results)

            if ordering_result.flag:
                return ResultLookup(True, ordering_result.value[0][0])
            if not any(ordering_result.value):
                return ResultLookup(errors=ordering_result.errors)
            ranked_results = ordering_result.value

        # if we've exhausted all ordering services, just pick a permutation at random
        return ResultLookup(True, ordering_result.value[0][0])

    def reset(self, turn_descriptor: TurnDescriptorLookup) -> None:
        self._reset_turn_descriptor(turn_descriptor)
        self._turn_descriptor_tiles = None

    def _cache_turn_descriptor_state(self, turn_descriptor: TurnDescriptorLookup) -> None:
        if self._turn_descriptor_tiles is not None:
            raise InvalidOperationError("cannot call _cache_turn_descriptor_state multiple times without reset()ing")
        self._turn_descriptor_tiles = list(turn_descriptor.tiles)

    def _reset_turn_descriptor(self, turn_descriptor: TurnDescriptorLookup) -> None:
        if self._turn_descriptor_tiles is None:
            raise InvalidOperationError("must call _cache_turn_descriptor_state before _reset_turn_descriptor_state")
        turn_descriptor.tiles.clear()
        turn_descriptor.tiles.extend(self._turn_descriptor_tiles)

    def _does_pass_all_constraints(
            self,
            permutation: List[BaseAction],
            constraint_validator: BaseConstraintValidator) -> bool:
        index_of_first_action = constraint_validator.get_index_of_first_action_which_fails_constraints(permutation)
        if index_of_first_action == -1:
            return True
        self._permutation_forge.mark_last_permutation_as_invalid(index_of_first_action)
#        print(f"[DBG] permutation does not pass constraints; failed at {index_of_first_action}")
#        for action in permutation[:index_of_first_action]:
#            print(f"[DBG]          action {action:8}")
#        print(f"[DBG] ## fail: action {permutation[index_of_first_action]:8}")
#        for action in permutation[index_of_first_action+1:]:
#            print(f"[DBG] skipped: action {action:8}")
#        print("[VRB]")
        return False
