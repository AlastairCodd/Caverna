from typing import List, cast, Dict, Union

from buisness_logic.services.available_dwarf_service import AvailableDwarfService
from buisness_logic.services.base_dwarf_player_choice_transfer_service import BaseDwarfPlayerChoiceTransferService
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.harvest_type_enum import HarvestTypeEnum


class CompleteDwarfPlayerChoiceTransferService(BaseDwarfPlayerChoiceTransferService):
    def __init__(self):
        self._available_dwarf_service: AvailableDwarfService = AvailableDwarfService()

    def get_dwarf(
            self,
            player: Player,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[Dwarf]:
        if player is None:
            raise ValueError

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
                        cards,
                        turn_index,
                        round_index,
                        harvest_type)

                errors.extend(player_choice_use_dwarf_out_of_order.errors)
                success = player_choice_use_dwarf_out_of_order.flag
                is_using_dwarf_of_lowest_level = not player_choice_use_dwarf_out_of_order.value

        dwarf: Union[Dwarf, None] = None
        if success:
            if is_using_dwarf_of_lowest_level:
                dwarf = available_dwarves_by_level[lowest_level_of_dwarves][0]
            else:
                player_choice_use_dwarf_out_of_order: ResultLookup[Dwarf] = \
                    player.get_player_choice_dwarf_to_use_out_of_order(
                        available_dwarves,
                        cards,
                        turn_index,
                        round_index,
                        harvest_type)

                success = player_choice_use_dwarf_out_of_order.flag
                errors.extend(player_choice_use_dwarf_out_of_order.errors)

                if player_choice_use_dwarf_out_of_order.flag:
                    dwarf = player_choice_use_dwarf_out_of_order.value

        result: ResultLookup[Dwarf] = ResultLookup(success, dwarf, errors)

        return result
