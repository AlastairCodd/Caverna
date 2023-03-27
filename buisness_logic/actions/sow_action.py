from typing import Dict, List, Optional

from buisness_logic.effects.allow_farming_effect import AllowFarmingEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.resources_to_sow_lookup import ResourcesToSow
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class SowAction(BasePlayerChoiceAction):
    def __init__(self) -> None:
        """Sow action which allows a number of food resources to be planted, and their amount increased."""
        self._resources_to_sow: Optional[ResourcesToSow] = None

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("Player may not be None")

        resources_to_sow_result: ResultLookup[ResourcesToSow] = player.get_player_choice_resources_to_sow(turn_descriptor)

        if not resources_to_sow_result.flag:
            return ResultLookup(errors=resources_to_sow_result.errors)

        success: bool = True
        errors: List[str] = []

        errors.extend(resources_to_sow_result.errors)

        if resources_to_sow_result.value.grain > 2:
            success = False
            errors.append(f"Attempted to sow more grain than allowed: attempted {resources_to_sow_result.value.grain}, permitted 2")
        if resources_to_sow_result.value.veg > 2:
            success = False
            errors.append(f"Attempted to sow more veg than allowed: attempted {resources_to_sow_result.value.veg}, permitted 2")

        if success:
            self._resources_to_sow = resources_to_sow_result.value

        result: ResultLookup[ActionChoiceLookup] = ResultLookup(success, ActionChoiceLookup([]), errors)
        return result

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Sows quantity seeds of some resource type, increasing the yield by the amount determined by "_grow_amount".

        :param player: The player who is planting the seeds. This cannot be null.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: A result lookup indicating the success of the action, and the number of seeds which were planted.
            This will never be null.
        """
        if player is None:
            raise ValueError("Player may not be None")

        farming_effects: List[AllowFarmingEffect] = [effect
                                                     for effect
                                                     in player.get_effects_of_type(AllowFarmingEffect)
                                                     if effect.can_plant]

        number_of_farming_effects: int = len(farming_effects)
        number_of_resources_to_sow: int = self._resources_to_sow.grain + self._resources_to_sow.veg

        if number_of_farming_effects < number_of_resources_to_sow:
            return ResultLookup(value=0, errors=f"Insufficient locations available for planting resources: attempted {len(self._resources_to_sow)}, permitted {number_of_farming_effects}")

        success: bool = True
        successes: int = 0
        errors: List[str] = []

        for (i, effect) in enumerate(farming_effects):
            if i >= number_of_resources_to_sow:
                break
            resource = ResourceTypeEnum.grain if i < self._resources_to_sow.grain else ResourceTypeEnum.veg
            plant_resource_result: ResultLookup[bool] = effect.plant_resource(player, resource)

            success &= plant_resource_result.flag
            errors.extend(plant_resource_result.errors)

            if plant_resource_result.flag:
                successes += 1

        result: ResultLookup[int] = ResultLookup(success, successes, errors)
        return result

    def new_turn_reset(self):
        self._resources_to_sow = None

    def __str__(self) -> str:
        return self.__format__("")

    def __format__(self, format_spec):
        text = [
            ("", "Sow up to "),
            ("class:count", "2"),
            ("", " "),
            ("class:resource", "grain"),
            ("", " or "),
            ("class:count", "2"),
            ("", " "),
            ("class:resource", "veg"),
        ]

        if "pp" in format_spec:
            return text
        return "".join(e[1] for e in text)
