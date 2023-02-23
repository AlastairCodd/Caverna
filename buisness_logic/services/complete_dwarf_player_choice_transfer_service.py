from typing import List, Dict, Tuple, Optional

from buisness_logic.actions.pay_action import PayAction
from buisness_logic.services.available_dwarf_service import AvailableDwarfService
from buisness_logic.services.base_dwarf_player_choice_transfer_service import BaseDwarfPlayerChoiceTransferService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.exceptions.invalid_operation_error import InvalidOperationError
from core.services.base_player_service import BasePlayerService


class CompleteDwarfPlayerChoiceTransferService(BaseDwarfPlayerChoiceTransferService):
    def __init__(self):
        self._available_dwarf_service: AvailableDwarfService = AvailableDwarfService()

    def get_dwarf(
            self,
            player: BasePlayerService,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[Tuple[Dwarf, ActionChoiceLookup]]:
        if player is None:
            raise ValueError("Player may not be null.")
        if turn_descriptor is None:
            raise ValueError("Turn descriptor may not be null.")

        available_dwarves: List[Dwarf] = [dwarf for dwarf in player.dwarves if not dwarf.is_active and dwarf.is_adult]

        if len(available_dwarves) == 0:
            raise IndexError("Player must have at least one dwarf available")

        lowest_level_of_dwarves: int
        available_dwarves_by_level: Dict[int, List[Dwarf]]
        available_dwarves_by_level, lowest_level_of_dwarves = self._available_dwarf_service.get_available_dwarves_by_level(player)

        does_player_have_dwarves_of_multiple_levels_available: bool = len(available_dwarves_by_level) > 1
        is_using_dwarf_of_lowest_level: bool = True

        success: bool = True
        errors: List[str] = []

        if does_player_have_dwarves_of_multiple_levels_available:
            does_player_meet_condition_to_use_dwarf_out_of_order: ResultLookup[bool] = self._available_dwarf_service.can_player_use_a_dwarf_out_of_order(player)
            if does_player_meet_condition_to_use_dwarf_out_of_order.flag:
                player_choice_use_dwarf_out_of_order: ResultLookup[bool] = \
                    player.get_player_choice_use_dwarf_out_of_order(
                        available_dwarves,
                        turn_descriptor)

                errors.extend(player_choice_use_dwarf_out_of_order.errors)
                success = player_choice_use_dwarf_out_of_order.flag
                is_using_dwarf_of_lowest_level = not player_choice_use_dwarf_out_of_order.value

        dwarf: Optional[Dwarf] = None
        additional_actions: List[BaseAction] = []

        if success:
            if is_using_dwarf_of_lowest_level:
                dwarf = available_dwarves_by_level[lowest_level_of_dwarves][0]
            else:
                player_choice_use_dwarf_out_of_order: ResultLookup[Dwarf] = \
                    player.get_player_choice_dwarf_to_use_out_of_order(
                        available_dwarves,
                        turn_descriptor)

                success = player_choice_use_dwarf_out_of_order.flag
                errors.extend(player_choice_use_dwarf_out_of_order.errors)

                if player_choice_use_dwarf_out_of_order.flag:
                    if player_choice_use_dwarf_out_of_order.value in available_dwarves:
                        dwarf = player_choice_use_dwarf_out_of_order.value

                        if dwarf.weapon_level != lowest_level_of_dwarves:
                            pay_dwarf_cost_action: BaseAction = PayAction({ResourceTypeEnum.ruby: 1})
                            additional_actions.append(pay_dwarf_cost_action)
                    else:
                        success = False
                        errors.append("Attempted to use dwarf that is already in use.")

        result: ResultLookup[Tuple[Dwarf, ActionChoiceLookup]]
        if success:
            if dwarf is None:
                raise InvalidOperationError("DEV ERROR: Success => dwarf is not none")
            result = ResultLookup(success, (dwarf, ActionChoiceLookup(additional_actions)), errors)
        else:
            result = ResultLookup(errors=errors)

        return result
