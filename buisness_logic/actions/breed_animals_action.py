from typing import Dict, List, Optional, Iterable, Tuple

from buisness_logic.effects.animal_storage_effects import BaseAnimalStorageEffect, ChangeAnimalStorageBaseEffect
from buisness_logic.effects.resource_effects import ReceiveWhenBreedingEffect
from buisness_logic.services.base_receive_event_service import BaseReceiveEventService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_entity import TileEntity
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.resource_layout_exhaustive_checker import ResourceLayoutExhaustiveChecker
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class BreedAnimalsAction(BasePlayerChoiceAction, BaseReceiveEventService):
    def __init__(self, maximum: int = 4) -> None:
        if maximum <= 0:
            raise ValueError("The maximum number of animals to breed must be positive.")
        if maximum > 4:
            raise ValueError("The maximum number of animals to breed cannot exceed the number of types of animals.")
        self._maximum_number_of_animals_to_reproduce = maximum

        self._resource_layout_checker: ResourceLayoutExhaustiveChecker = ResourceLayoutExhaustiveChecker()

        self._animals_which_can_reproduce: List[ResourceTypeEnum] = [
            ResourceTypeEnum.sheep,
            ResourceTypeEnum.donkey,
            ResourceTypeEnum.boar,
            ResourceTypeEnum.cow,
        ]

        self._animals_to_reproduce: Optional[List[ResourceTypeEnum]] = None

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
            self._animals_which_can_reproduce,
            self._maximum_number_of_animals_to_reproduce,
            turn_descriptor)

        result: ResultLookup[ActionChoiceLookup]
        if animals_to_reproduce_result.flag:
            if len(animals_to_reproduce_result.value) > self._maximum_number_of_animals_to_reproduce:
                result = ResultLookup(
                    errors=f"Attempted to breed more than {self._maximum_number_of_animals_to_reproduce} animals")
            else:
                self._animals_to_reproduce = animals_to_reproduce_result.value
                result = ResultLookup(True, ActionChoiceLookup([], []))
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

        if success:
            # pasture	                                        2	any		tile effect
            # large pasture	                                    4	any		tile effect
            # entry level dwelling	                            2	any		tile effect
            # mine	                                            1	donkey	tile effect

            # meadow	                                        0	any		default
            # forest	                                        0	any		default

            # pasture with stable	    previous capacity times 2	any		condition
            # meadow with stable	                            1	any		condition... change animal storage base effect?
            # forest with stable	                            1	boar	condition... change animal storage base effect?

            # dog in meadow	            number of dogs on tile +1	sheep	dog effect
            # dog in pasture	        number of dogs on tile +1	sheep	dog effect
            # dog on tile with stable	number of dogs on tile +1	sheep	dog effect
            does_player_have_space_for_animals_result: ResultLookup[bool] = self\
                ._does_player_have_space_for_animals(player)
            success &= does_player_have_space_for_animals_result.flag
            errors.extend(does_player_have_space_for_animals_result.errors)

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

    def _does_player_have_space_for_animals(
            self,
            player: BasePlayerRepository) -> ResultLookup[bool]:
        animal_storage_buckets: List[Dict[ResourceTypeEnum, int]] = self._get_animal_storage_buckets_for_player(player)
        player_animals: Dict[ResourceTypeEnum, int] = {
            animal: player.get_resources_of_type(animal)
            for animal
            in self._animals_which_can_reproduce
            if player.get_resources_of_type(animal) > 0}

        evaluated_partitions: Iterable[
            Tuple[
                bool,
                List[Optional[ResourceTypeEnum]],
                Dict[ResourceTypeEnum, int],
                Dict[ResourceTypeEnum, int]
            ]
        ] = self._resource_layout_checker \
            .check_resource_layout_against_possible_set_partitions(
                animal_storage_buckets,
                player_animals)

        success: bool = False
        for (did_partition_store_all_animals, partition, remaining, excess) in evaluated_partitions:
            if did_partition_store_all_animals:
                success = True
                break

        result: ResultLookup[bool]
        if success:
            result = ResultLookup(True, True)
        else:
            result = self._does_player_have_space_for_animals_with_dogs(
                player,
                player_animals,
                animal_storage_buckets)
        return result

    def _does_player_have_space_for_animals_with_dogs(
            self,
            player: BasePlayerRepository,
            player_animals: Dict[ResourceTypeEnum, int],
            dogless_layout: Dict[int, Dict[ResourceTypeEnum, int]]) -> ResultLookup[bool]:
        # self._get_tiles_which_dogs_have_effect_on()

        animal_storage_buckets: List[Dict[ResourceTypeEnum, int]] = self._get_animal_storage_buckets_for_player(player)
        player_animals: Dict[ResourceTypeEnum, int] = {
            animal: player.get_resources_of_type(animal)
            for animal
            in self._animals_which_can_reproduce
            if player.get_resources_of_type(animal) > 0}
        evaluated_partitions: Iterable[
            Tuple[
                bool,
                List[Optional[ResourceTypeEnum]],
                Dict[ResourceTypeEnum, int],
                Dict[ResourceTypeEnum, int]
            ]
        ] = self._resource_layout_checker \
            .check_resource_layout_against_possible_set_partitions(
            animal_storage_buckets,
            player_animals)
        success: bool = False
        for (did_partition_store_all_animals, partition, remaining, excess) in evaluated_partitions:
            if did_partition_store_all_animals:
                success = True
                break
        if success:
            result = ResultLookup(True, True)
        else:
            result = ResultLookup(errors="Player does not have enough space to store all animals")
        return result

    def _get_animal_storage_buckets_for_player(
            self,
            player: BasePlayerRepository) -> List[Dict[ResourceTypeEnum, int]]:
        if player is None:
            raise ValueError("Player cannot be none")

        base_animal_storage_effects: List[ChangeAnimalStorageBaseEffect] = player\
            .get_effects_of_type(ChangeAnimalStorageBaseEffect)

        buckets: List[Dict[ResourceTypeEnum, int]] = []

        for tile in player.tiles.values():
            bucket_for_tile: Dict[ResourceTypeEnum, int] = self._get_animal_storage_buckets_for_tile(
                base_animal_storage_effects,
                player,
                tile)
            if any(bucket_for_tile.values()):
                buckets.append(bucket_for_tile)

        return buckets

    def _get_animal_storage_buckets_for_tile(
            self,
            base_animal_storage_effects: List[ChangeAnimalStorageBaseEffect],
            player: BasePlayerRepository,
            tile: TileEntity,
            number_of_dogs_on_tile: int = 0) -> Dict[ResourceTypeEnum, int]:
        if base_animal_storage_effects is None:
            raise ValueError("Base storage effects cannot be none")
        if player is None:
            raise ValueError("Player cannot be none")
        if tile is None:
            raise ValueError("Tile cannot be none")

        animal_storage_effects_for_tile: List[BaseAnimalStorageEffect] = tile.get_effects_of_type(
            BaseAnimalStorageEffect)

        storage_for_tile: Dict[ResourceTypeEnum, int] = {animal: 0 for animal in self._animals_which_can_reproduce}
        if len(animal_storage_effects_for_tile) > 0:
            for effect in animal_storage_effects_for_tile:
                new_buckets: Dict[ResourceTypeEnum, int] = effect.get_animal_storage_buckets(player)
                self._update_storage_for_tile(
                    new_buckets,
                    storage_for_tile)
            if tile.has_stable:
                for animal in storage_for_tile:
                    storage_for_tile[animal] *= 2
        else:
            for effect in base_animal_storage_effects:
                new_buckets_result: ResultLookup[Dict[ResourceTypeEnum, int]] = effect\
                    .get_animal_storage_buckets_for_tile(
                        player,
                        tile)

                if new_buckets_result:
                    new_buckets: Dict[ResourceTypeEnum, int] = new_buckets_result.value
                    self._update_storage_for_tile(
                        new_buckets,
                        storage_for_tile)

        if number_of_dogs_on_tile > storage_for_tile[ResourceTypeEnum.sheep]:
            storage_for_tile[ResourceTypeEnum.sheep] = number_of_dogs_on_tile

        return storage_for_tile

    def _update_storage_for_tile(
            self,
            new_buckets,
            storage_for_tile):
        for animal in new_buckets:
            current_storage_for_animal: int = storage_for_tile[animal]
            new_storage_for_animal: int = new_buckets[animal]
            if new_storage_for_animal > current_storage_for_animal:
                storage_for_tile[animal] = new_storage_for_animal

    def new_turn_reset(self):
        self._animals_to_reproduce = None
