from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class GiveDwarfAWeaponAction(BasePlayerChoiceAction):

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        # TODO: Implement this
        player.get_effects_of_type()
        max_attainable_level = player.get_resources_of_type(ResourceTypeEnum.ore)
        chosen_weapon_level = player.get_player_choice_weapon_level()

        raise NotImplementedError()

    def invoke(
            self,
            player: BasePlayerRepository,
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
            raise ValueError("Player may not be none/")

        raise NotImplementedError()

    def new_turn_reset(self):
        pass
