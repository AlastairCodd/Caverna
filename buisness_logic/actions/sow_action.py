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

        self._sowable_resources: List[ResourceTypeEnum] = [ResourceTypeEnum.veg, ResourceTypeEnum.grain]

        self._resources_to_sow: List[ResourceTypeEnum] = []

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("Player may not be None")

        resources_to_sow_result: ResultLookup[List[ResourceTypeEnum]] = player.get_player_choice_resources_to_sow(
            self._quantity,
            turn_descriptor)

        success: bool = resources_to_sow_result.flag
        errors: List[str] = []

        errors.extend(resources_to_sow_result.errors)

        if resources_to_sow_result.flag:
            is_attempted_number_of_resources_in_range: bool = len(resources_to_sow_result.value) <= self._quantity
            invalid_resources: List[ResourceTypeEnum] = [resource for resource in resources_to_sow_result.value if resource not in self._sowable_resources]

            if not is_attempted_number_of_resources_in_range:
                success = False
                errors.append(f"Attempted to sow more resources than was permitted: attempted {len(resources_to_sow_result.value)}, permitted {self._quantity}")

            if any(invalid_resources):
                success = False
                for invalid_resource in invalid_resources:
                    errors.append(f"Attempted to sow resource which cannot be sown: resource {invalid_resource.name}")

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

        success: bool = True
        successes: int = 0
        errors: List[str] = []

        farming_effects: List[AllowFarmingEffect] = [effect
                                                     for effect
                                                     in player.get_effects_of_type(AllowFarmingEffect)
                                                     if effect.can_plant]

        number_of_farming_effects: int = len(farming_effects)
        if number_of_farming_effects >= len(self._resources_to_sow):
            for effect, resource in zip(farming_effects, self._resources_to_sow):
                plant_resource_result: ResultLookup[bool] = effect.plant_resource(player, resource)
                success &= plant_resource_result.flag
                errors.extend(plant_resource_result.errors)

                if plant_resource_result.flag:
                    successes += 1
        else:
            success = False
            errors.append(
                f"Insufficient locations available for planting resources: attempted {len(self._resources_to_sow)}, permitted {number_of_farming_effects}")

        result: ResultLookup[int] = ResultLookup(success, successes, errors)
        return result

    def new_turn_reset(self):
        self._resources_to_sow.clear()

    def __str__(self) -> str:
        return f"Sow {self._quantity} resources"
