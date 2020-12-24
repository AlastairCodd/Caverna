from typing import List, Optional, Dict

from buisness_logic.effects.purchase_effects import DecreasePriceOfWeaponEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.entities.weapon import Weapon
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class GiveDwarfAWeaponAction(BasePlayerChoiceAction):
    def __init__(self):
        self._level_of_weapon: Optional[int] = None

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        chosen_weapon_level: int = player.get_player_choice_weapon_level(turn_descriptor)

        is_chosen_weapon_level_within_bounds: bool = 0 < chosen_weapon_level <= 8

        if is_chosen_weapon_level_within_bounds:
            result = ResultLookup(True, ActionChoiceLookup([], []))
            self._level_of_weapon = chosen_weapon_level
        else:
            result = ResultLookup(errors=f"Chosen weapon level ({chosen_weapon_level}) is not in bounds")
        return result

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
            raise ValueError("Player may not be none")
        if current_dwarf is None:
            raise ValueError("Current dwarf may not be none")
        if self._level_of_weapon is None:
            raise ValueError("Must have chosen player option")

        cost_of_weapon: Dict[ResourceTypeEnum, int] = {ResourceTypeEnum.ore: self._level_of_weapon}
        effects: List[DecreasePriceOfWeaponEffect] = player.get_effects_of_type(DecreasePriceOfWeaponEffect)

        for effect in effects:
            cost_of_weapon = effect.invoke(cost_of_weapon)

        for resource in cost_of_weapon:
            if cost_of_weapon[resource] < 0:
                cost_of_weapon[resource] = 0

        errors: List[str] = []

        can_player_afford_weapon: bool = player.has_more_resources_than(cost_of_weapon)
        if not can_player_afford_weapon:
            errors.append(f"Player cannot afford weapon (\r\ncost: {cost_of_weapon},\r\n" +
                          f"player resources: {player.resources})")

        if current_dwarf.has_weapon:
            errors.append("Dwarf already has a weapon")

        success: bool = len(errors) == 0

        if success:
            weapon_for_dwarf: Weapon = Weapon(self._level_of_weapon)
            current_dwarf.give_weapon(weapon_for_dwarf)

            success &= player.take_resources(cost_of_weapon)
            if not success:
                errors.append("Failed to take resources from player")

        result: ResultLookup[int] = ResultLookup(True, 1) if success else ResultLookup(errors=errors)
        return result

    def new_turn_reset(self):
        self._level_of_weapon = None
