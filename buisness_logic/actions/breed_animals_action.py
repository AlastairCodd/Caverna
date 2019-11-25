from typing import Dict, List
from buisness_logic.effects.animal_storage_effects import BaseAnimalStorageEffect
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum


class BreedAnimalsAction(BaseAction):
    def __init__(self, maximum=4):
        if maximum < 0 or maximum > 4:
            raise ValueError("maximum")
        self._maximum = maximum

    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
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
        if len(animals_which_can_reproduce) > self._maximum:
            animals_to_reproduce = player.get_player_choice_breed_animals(animals_which_can_reproduce, self._maximum)
        else:
            animals_to_reproduce = animals_which_can_reproduce

        raise NotImplementedError()

    def new_turn_reset(self):
        pass
