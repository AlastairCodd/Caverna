from typing import Dict, List, Optional

from buisness_logic.actions.base_receive_action import BaseReceiveAction
from buisness_logic.effects.resource_effects import ReceiveWhenBreedingEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.constants import resource_types
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class BreedAnimalsAction(BaseReceiveAction):
    def __init__(self, maximum: int = 4) -> None:
        if maximum <= 0:
            raise ValueError("The maximum number of animals to breed must be positive.")
        if maximum > 4:
            raise ValueError("The maximum number of animals to breed cannot exceed the number of types of animals.")
        self._maximum_number_of_animals_to_reproduce = maximum

        self._animals_to_reproduce: Optional[List[ResourceTypeEnum]] = None
        BaseReceiveAction.__init__(self, {animal: 1 for animal in resource_types.farm_animals})

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("Player cannot be none")
        if turn_descriptor is None:
            raise ValueError("Turn descriptor cannot be none")

        animals_to_reproduce_result: ResultLookup[List[ResourceTypeEnum]] = player.get_player_choice_animals_to_breed(
            resource_types.farm_animals,
            self._maximum_number_of_animals_to_reproduce,
            turn_descriptor)

        result: ResultLookup[ActionChoiceLookup]
        if animals_to_reproduce_result.flag:
            if len(animals_to_reproduce_result.value) > self._maximum_number_of_animals_to_reproduce:
                result = ResultLookup(
                    errors=f"Attempted to breed more than {self._maximum_number_of_animals_to_reproduce} animals")
            else:
                self._animals_to_reproduce = animals_to_reproduce_result.value
                result = BaseReceiveAction.set_player_choice(self, player, dwarf, turn_descriptor)
        else:
            result = ResultLookup(errors=animals_to_reproduce_result.errors)
        return result

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Gives the player an additional farm animal, provided they have at least two and space. 

        :param player: The player who will buy things. This may not be null.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: True if player chosen items were successfully purchased, false if not.
        """
        if player is None:
            raise ValueError("Player may not be none")
        if self._animals_to_reproduce is None:
            raise ValueError("Must choose a animals to reproduce (_animals_to_reproduce)")

        success: bool = True
        value: int = 0
        errors: List[str] = []

        does_player_have_enough_animals_result: ResultLookup[bool] = self._does_player_have_enough_animals(player)
        success &= does_player_have_enough_animals_result.flag
        errors.extend(does_player_have_enough_animals_result.errors)

        if success:
            increase_number_of_animals_result: ResultLookup[int] = self._increase_number_of_animals_player_has(player)

            success &= increase_number_of_animals_result.flag
            value = increase_number_of_animals_result.value
            errors.extend(increase_number_of_animals_result.errors)

        success: bool = len(errors) == 0
        result: ResultLookup[int] = ResultLookup(True, value) if success else ResultLookup(errors=errors)
        return result

    def _does_player_have_enough_animals(
            self,
            player: BasePlayerRepository) -> ResultLookup[bool]:
        success: bool = True
        errors: List[str] = []

        for animal in self._animals_to_reproduce:
            number_of_animals: int = player.get_resources_of_type(animal)
            if number_of_animals < 2:
                success = False
                errors.append(
                    f"Attempted to breed {animal.name} but did not have a pair (current number: {number_of_animals})")

        result: ResultLookup[bool] = ResultLookup(success, success, errors)
        return result

    def _increase_number_of_animals_player_has(
            self,
            player: BasePlayerRepository) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player cannot be None")

        new_animals: Dict[ResourceTypeEnum, int] = {animal: 1 for animal in self._animals_to_reproduce}
        give_player_resources_result: ResultLookup[int] = self._give_player_resources(player, new_animals)

        result: ResultLookup[int] = give_player_resources_result
        if give_player_resources_result.flag:
            effects: List[ReceiveWhenBreedingEffect] = player.get_effects_of_type(ReceiveWhenBreedingEffect)

            if len(effects) > 0:
                success: bool = True
                value: int = give_player_resources_result.value
                errors: List[str] = []
                for effect in effects:
                    breeding_effect_result: ResultLookup[int] = effect.invoke(player, self._animals_to_reproduce)

                    success &= breeding_effect_result.flag
                    value += breeding_effect_result.value
                    errors.extend(breeding_effect_result.errors)

                result = ResultLookup(success, value, errors)

        return result

    def new_turn_reset(self):
        self._animals_to_reproduce = None
