from buisness_logic.effects.population_effects import *
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard


class GetABabyDwarfAction(BaseAction):
    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
        """Gives player a new dwarf, if they have room.

        :param player: The player to give the new dwarf to. This may not be none.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: True if a new dwarf has been born, false if not.
        """
        if player is None:
            raise ValueError("player")

        numberOfDwarves: int = len(player.dwarves)

        increase_population_maximum_effects = player.get_effects_of_type(IncreasePopulationMaximumEffect)
        maximum_population: int = 5 + sum(map(
            lambda effect: effect.raise_maximum_population_by,
            increase_population_maximum_effects))

        increase_population_capacity_effects = player.get_effects_of_type(IncreasePopulationCapacityEffect)
        player_population_capacity: int = sum(map(
            lambda effect: effect.capacity,
            increase_population_capacity_effects))

        result: ResultLookup[int]
        if numberOfDwarves < maximum_population:
            if numberOfDwarves < player_population_capacity:
                player.give_baby_dwarf()
                result = ResultLookup(True, 1)
            else:
                result = ResultLookup(False, 0, "Currently no room for more dwarves")
        else:
            result = ResultLookup(False, 0, "Maximum number of dwarves reached")

        return result

    def new_turn_reset(self):
        pass
