from buisness_logic.effects.population_effects import *
from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainer


class GetABabyDwarfAction(BaseAction):
    def invoke(self, player: Player, active_card: ResourceContainer) -> bool:
        """Gives player a new dwarf, if they have room.

        :param player: The player to give the new dwarf to. This may not be none.
        :param active_card: Unused.
        :return: True if a new dwarf has been born, false if not.
        """
        if player is None:
            raise ValueError("player")

        result: bool = False
        numberOfDwarves: int = len(player.dwarves)
        if numberOfDwarves <= 5:
            populationCap: int = len(player.get_effects_of_type(IncreasePopulationCapEffect))
            if numberOfDwarves < populationCap:
                player.give_baby_dwarf()
                result = True
        elif numberOfDwarves == 6:
            sixthDwarfAllowed: bool = any(player.get_effects_of_type(AllowSixthDwarfEffect))
            if sixthDwarfAllowed:
                player.give_baby_dwarf()
                result = True
        return result

    def new_turn_reset(self):
        pass
