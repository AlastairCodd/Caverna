from typing import Dict, List

from buisness_logic.effects.animal_storage_effects import BaseAnimalStorageEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class BreedAnimalsAction(BasePlayerChoiceAction):
    def __init__(self, maximum: int = 4) -> None:
        if maximum <= 0:
            raise ValueError("The maximum number of animals to breed must be positive.")
        if maximum > 4:
            raise ValueError("The maximum number of animals to breed cannot exceed the number of types of animals.")
        self._maximum = maximum

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        # TODO: Implement this
        raise NotImplementedError()

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
        player_farm_animals: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.sheep: player.get_resources_of_type(ResourceTypeEnum.sheep),
            ResourceTypeEnum.donkey: player.get_resources_of_type(ResourceTypeEnum.donkey),
            ResourceTypeEnum.ore: player.get_resources_of_type(ResourceTypeEnum.ore),
            ResourceTypeEnum.cow: player.get_resources_of_type(ResourceTypeEnum.cow)}

        animals_which_can_reproduce: List[ResourceTypeEnum] = []

        for animal, quantity in player_farm_animals.items():
            if quantity >= 2:
                animals_which_can_reproduce.append(animal)

        animal_storage_effect: BaseAnimalStorageEffect
        animal_storage_buckets: List[Dict[ResourceTypeEnum, int]] = []
        for animal_storage_effect in player.get_effects_of_type(BaseAnimalStorageEffect):
            buckets: List[Dict[ResourceTypeEnum, int]] = animal_storage_effect.get_animal_storage_buckets(player)
            for bucket in buckets:
                animal_storage_buckets.append(bucket)

        animals_to_reproduce: List[ResourceTypeEnum]
        # TODO: Implement and test this
        if len(animals_which_can_reproduce) > self._maximum:
            animals_to_reproduce = player.get_player_choice_breed_animals(
                animals_which_can_reproduce,
                self._maximum)
        else:
            animals_to_reproduce = animals_which_can_reproduce

        raise NotImplementedError()

    def new_turn_reset(self):
        pass
