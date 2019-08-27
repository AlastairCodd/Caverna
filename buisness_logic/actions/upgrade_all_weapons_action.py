from common.entities.dwarf import Dwarf
from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainer


class UpgradeAllWeaponsAction(BaseAction):
    def invoke(self, player: Player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
        """Increases the level of all weapons owned by dwarves.

        :param player: The player who has dwarves. This may not be null.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: False if no dwarves can have weapons upgraded, true otherwise.
        """
        if player is None:
            raise ValueError(str(player))
        does_player_have_any_dwarves_with_weapons: bool = False
        have_all_weapons_been_successfully_upgraded: bool = True

        for dwarf in player.dwarves:
            if dwarf.has_weapon:
                does_player_have_any_dwarves_with_weapons = True
                have_all_weapons_been_successfully_upgraded &= dwarf.weapon_level == dwarf.weapon.increase_level()

        result = does_player_have_any_dwarves_with_weapons and have_all_weapons_been_successfully_upgraded
        return result

    def new_turn_reset(self):
        pass
