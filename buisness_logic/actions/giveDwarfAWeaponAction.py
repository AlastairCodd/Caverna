from typing import List

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class GiveDwarfAWeaponAction(BasePlayerChoiceAction):

    def set_player_choice(
            self,
            player: Player,
            dwarf: Dwarf,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        player.get_effects_of_type()
        max_attainable_level = player.get_resources_of_type(ResourceTypeEnum.ore)
        chosen_weapon_level = player.get_player_choice_weapon_level()

        raise NotImplementedError()

    def invoke(
            self,
            player: Player,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
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

        raise NotImplementedError()

    def new_turn_reset(self):
        pass
