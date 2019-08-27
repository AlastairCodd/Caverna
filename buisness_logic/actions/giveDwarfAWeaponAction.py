from common.entities.dwarf import Dwarf
from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum


class GiveDwarfAWeaponAction(BaseAction):

    def invoke(self, player: Player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
        """Gives the current dwarf a weapon.
        Player provides n ore (0<n<8), and exchanges it for a weapon with the same level.
        If player has any ore discount effects, these are applied to reduce the cost.
        Maximum weapon strength is limited at 8 (page a4 of appendix)"

        :param player: The player. This cannot be null.
        :param active_card: Unused.
        :param current_dwarf: The dwarf who is given the weapon.
        :returns: True if the dwarf was given a weapon with the intended level, false if not.
        """
        if player is None:
            raise ValueError("player")

        player.get_effects_of_type()
        max_attainable_level = player.get_resources_of_type(ResourceTypeEnum.ore)
        chosen_weapon_level = player.get_player_choice_weapon_level()

        raise NotImplementedError()

    def new_turn_reset(self):
        pass
