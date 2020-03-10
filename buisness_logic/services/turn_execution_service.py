from typing import List

from buisness_logic.services.available_dwarf_service import AvailableDwarfService
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from common.services.action_invoke_service import ActionInvokeService
from core.baseClasses.base_card import BaseCard
from core.constants import game_constants
from core.enums.harvest_type_enum import HarvestTypeEnum


class TurnExecutionService(object):
    def __init__(self):
        self._actionInvokeService: ActionInvokeService = ActionInvokeService()
        self._available_dwarf_service: AvailableDwarfService = AvailableDwarfService()
        self.number_of_rounds: int = game_constants.number_of_rounds

    def take_turn(
            self,
            player: Player,
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum,
            cards: List[BaseCard]) -> ResultLookup[Player]:
        if player is None:
            raise ValueError
        if turn_index >= len(player.dwarves):
            raise IndexError(f"Turn Index ({turn_index}) must be less than number of dwarves ({len(player.dwarves)})")
        if round_index >= self.number_of_rounds:
            raise IndexError(f"Maximum number of turns of ")

        success: bool = True
        errors: List[str] = []

        use_dwarf_out_of_order: bool = False
        if self._available_dwarf_service.can_player_use_a_dwarf_out_of_order(player):
            dwarf_out_of_order_result: ResultLookup[bool] = player.get_player_choice_use_dwarf_out_of_order()
            if dwarf_out_of_order_result.flag:
                use_dwarf_out_of_order = dwarf_out_of_order_result.value
            else:
                success = False
                errors.extend(dwarf_out_of_order_result.errors)

        available_dwarves: List[Dwarf] = []
        if success:
            available_dwarves_result: ResultLookup[List[Dwarf]] = self._available_dwarf_service \
                .get_available_dwarves(
                    player.dwarves,
                    use_dwarf_out_of_order)

            if not available_dwarves_result.flag:
                success = False
                errors.extend(available_dwarves_result.errors)
            else:
                available_dwarves = available_dwarves_result.value

        current_dwarf: Dwarf = None
        if success:
            if len(available_dwarves) == 1:
                current_dwarf = available_dwarves[0]
            else:
                dwarf_result: ResultLookup[Dwarf] = player.get_player_choice_dwarves(available_dwarves)
                if not dwarf_result.flag:
                    success = False
                    errors.extend(dwarf_result.errors)
                else:
                    current_dwarf = dwarf_result.value

        if success:
            player.get_player_choice_action(cards)
