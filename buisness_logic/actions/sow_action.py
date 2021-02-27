from typing import Dict, List

from buisness_logic.effects.allow_farming_effect import AllowFarmingEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class SowAction(BasePlayerChoiceAction):
    def __init__(
            self,
            quantity: int = 3) -> None:
        """Sow action which allows a number of food resources to be planted, and their amount increased.

        :param quantity: Upper bound on number of seeds which can be planted. Must be positive.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self._quantity: int = quantity

        self._resources_to_sow: List[ResourceTypeEnum] = []
        self._locations_to_sow: List[int] = []

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("Player may not be None")

        locations_to_sow_result: ResultLookup[List[int]] = player.get_player_choice_locations_to_sow(
            self._quantity,
            turn_descriptor)

        success: bool = locations_to_sow_result.flag
        errors: List[str] = []

        errors.extend(locations_to_sow_result.errors)

        if success:
            resources_to_sow_result: ResultLookup[List[ResourceTypeEnum]] = player.get_player_choice_resources_to_sow(
                len(locations_to_sow_result.value),
                turn_descriptor)

            success &= resources_to_sow_result.flag
            errors.extend(resources_to_sow_result.errors)

            if resources_to_sow_result.flag:
                self._locations_to_sow = locations_to_sow_result.value
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

        success: bool = True
        successes: int = 0
        errors: List[str] = []

        for resource_index in range(len(self._resources_to_sow)):
            resource_to_sow: ResourceTypeEnum = self._resources_to_sow[resource_index]
            location_to_sow: int = self._locations_to_sow[resource_index]

            farming_effects: List[AllowFarmingEffect] = [effect
                                                         for effect
                                                         in player.tiles[location_to_sow]
                                                             .get_effects_of_type(AllowFarmingEffect)
                                                         if effect.can_plant]
            if len(farming_effects) == 0:
                success = False
                errors.append(f"Cannot plant any resources on {location_to_sow}")
            else:
                plant_resource_result: ResultLookup[bool] = farming_effects[1].plant_resource(player, resource_to_sow)
                success &= plant_resource_result.flag
                errors.extend(plant_resource_result.errors)

                if plant_resource_result.flag:
                    successes += 1

        result: ResultLookup[int] = ResultLookup(success, successes, errors)
        return result

    def new_turn_reset(self):
        self._resources_to_sow.clear()
        self._locations_to_sow.clear()
