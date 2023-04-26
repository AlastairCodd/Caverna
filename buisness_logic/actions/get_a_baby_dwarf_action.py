from typing import List

from buisness_logic.effects.population_effects import *
from common.entities.dwarf import Dwarf
from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.constants import game_constants


class GetABabyDwarfAction(BaseAction):
    def __init__(self) -> None:
        BaseAction.__init__(self, "GetABabyDwarfAction")

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Gives player a new dwarf, if they have room.

        :param player: The player to give the new dwarf to. This may not be none.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: True if a new dwarf has been born, false if not.
        """
        if player is None:
            raise ValueError("player")

        number_of_dwarves: int = len(player.dwarves)

        increase_population_maximum_effects: List[IncreasePopulationMaximumEffect] = player.get_effects_of_type(IncreasePopulationMaximumEffect)
        maximum_population: int = game_constants.soft_maximum_number_of_dwarves + sum(map(
            lambda effect: effect.raise_maximum_population_by,
            increase_population_maximum_effects))

        increase_population_capacity_effects: List[IncreasePopulationCapacityEffect] = player.get_effects_of_type(IncreasePopulationCapacityEffect)
        player_population_capacity: int = sum(map(
            lambda effect: effect.capacity,
            increase_population_capacity_effects))

        result: ResultLookup[int]
        if number_of_dwarves < maximum_population:
            if number_of_dwarves < player_population_capacity:
                player.give_baby_dwarf()
                result = ResultLookup(True, 1)
            else:
                result = ResultLookup(False, 0, "Currently no room for more dwarves")
        else:
            result = ResultLookup(False, 0, "Maximum number of dwarves reached")

        return result

    def new_turn_reset(self):
        pass

    def __str__(self) -> str:
        return "Get a baby dwarf"
