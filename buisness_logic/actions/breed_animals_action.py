from typing import Dict, List, Optional, Iterable, Tuple, cast

from buisness_logic.effects.animal_storage_effects import BaseAnimalStorageEffect, ChangeAnimalStorageBaseEffect
from buisness_logic.effects.resource_effects import ReceiveWhenBreedingEffect
from buisness_logic.services.base_receive_event_service import BaseReceiveEventService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_entity import TileEntity
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.forges.integer_partition_forge import IntegerPartitionForge
from common.services.integer_partition_permutation_forge import IntegerPartitionPermutationForge
from common.services.resource_layout_exhaustive_checker import ResourceLayoutExhaustiveChecker
from common.services.resource_layout_polynomial_checker import ResourceLayoutPolynomialChecker
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.baseClasses.base_tile import BaseTwinTile
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService
from core.services.resource_layout_check_service import ResourceLayoutCheckService


class BreedAnimalsAction(BasePlayerChoiceAction, BaseReceiveEventService):
    def __init__(self, maximum: int = 4) -> None:
        if maximum <= 0:
            raise ValueError("The maximum number of animals to breed must be positive.")
        if maximum > 4:
            raise ValueError("The maximum number of animals to breed cannot exceed the number of types of animals.")
        self._maximum_number_of_animals_to_reproduce = maximum

        self._resource_layout_checker: ResourceLayoutCheckService = ResourceLayoutPolynomialChecker()
        # self._resource_layout_checker: ResourceLayoutCheckService = ResourceLayoutExhaustiveChecker()
        self._integer_partition_forge: IntegerPartitionForge = IntegerPartitionForge()
        self._integer_partition_permutation_forge: IntegerPartitionPermutationForge = IntegerPartitionPermutationForge()

        self._animals_which_can_reproduce: List[ResourceTypeEnum] = [
            ResourceTypeEnum.sheep,
            ResourceTypeEnum.donkey,
            ResourceTypeEnum.boar,
            ResourceTypeEnum.cow,
        ]

        self._tile_types_dogs_can_effect: List[TileTypeEnum] = [
            TileTypeEnum.meadow,
            TileTypeEnum.pasture,
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
            does_player_have_space_for_animals_result: ResultLookup[bool] = self \
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
        animal_storage_buckets: Dict[int, Dict[ResourceTypeEnum, int]] = self._get_animal_storage_buckets_for_player(player)
        player_animals: Dict[ResourceTypeEnum, int] = {
            animal: player.get_resources_of_type(animal)
            for animal
            in self._animals_which_can_reproduce
            if player.get_resources_of_type(animal) > 0}

        evaluated_partitions: Iterable[Tuple[
            bool,
            Dict[int, Optional[ResourceTypeEnum]],
            Dict[ResourceTypeEnum, int],
            Dict[ResourceTypeEnum, int]
        ]] = self._resource_layout_checker \
            .check_resource_layout(
            animal_storage_buckets,
            player_animals)

        player_has_sheep: bool = ResourceTypeEnum.sheep in player_animals
        minimal_missing_sheep: int = player.get_resources_of_type(ResourceTypeEnum.sheep)
        success: bool = False

        for (did_partition_store_all_animals, _, remaining, excess) in evaluated_partitions:
            if did_partition_store_all_animals:
                success = True
                break
            if player_has_sheep \
                    and not any(remaining[animal] > 0 for animal in remaining if not animal == ResourceTypeEnum.sheep)\
                    and remaining[ResourceTypeEnum.sheep] < minimal_missing_sheep:
                minimal_missing_sheep = remaining[ResourceTypeEnum.sheep]

        result: ResultLookup[bool]
        if success:
            result = ResultLookup(True, True)
        elif minimal_missing_sheep <= player.get_resources_of_type(ResourceTypeEnum.dog) * 2:
            result = self._does_player_have_space_for_animals_with_dogs(
                player,
                player_animals,
                animal_storage_buckets)
        else:
            result = ResultLookup(errors="Player does not have enough space to store all animals")

        return result

    def _get_animal_storage_buckets_for_player(
            self,
            player: BasePlayerRepository) -> Dict[int, Dict[ResourceTypeEnum, int]]:
        if player is None:
            raise ValueError("Player cannot be none")

        base_animal_storage_effects: List[ChangeAnimalStorageBaseEffect] = player \
            .get_effects_of_type(ChangeAnimalStorageBaseEffect)

        buckets: Dict[int, Dict[ResourceTypeEnum, int]] = {}

        for location, tile in player.tiles.items():
            bucket_for_tile: Dict[ResourceTypeEnum, int] = self._get_animal_storage_buckets_for_tile(
                base_animal_storage_effects,
                player,
                tile)
            if any(bucket_for_tile.values()):
                buckets[location] = bucket_for_tile

        return buckets

    def _get_animal_storage_buckets_for_tile(
            self,
            base_animal_storage_effects: List[ChangeAnimalStorageBaseEffect],
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> Dict[ResourceTypeEnum, int]:
        if base_animal_storage_effects is None:
            raise ValueError("Base storage effects cannot be none")
        if player is None:
            raise ValueError("Player cannot be none")
        if tile_entity is None:
            raise ValueError("Tile cannot be none")

        storage_for_tile: Dict[ResourceTypeEnum, int] = {}
        if tile_entity.tile is not None:
            is_tile_twin: bool = isinstance(tile_entity.tile, BaseTwinTile)
            is_primary_tile: bool = not is_tile_twin or cast(BaseTwinTile, tile_entity.tile).primary_tile_id == tile_entity.id

            if is_primary_tile:
                animal_storage_effects_for_tile: List[BaseAnimalStorageEffect] = tile_entity.get_effects_of_type(
                    BaseAnimalStorageEffect)

                storage_for_tile = {animal: 0 for animal in self._animals_which_can_reproduce}
                if len(animal_storage_effects_for_tile) > 0:
                    for effect in animal_storage_effects_for_tile:
                        new_buckets: Dict[ResourceTypeEnum, int] = effect.get_animal_storage_buckets(player)
                        self._update_storage_for_tile(
                            new_buckets,
                            storage_for_tile)
                    if tile_entity.has_stable:
                        for animal in storage_for_tile:
                            storage_for_tile[animal] *= 2
                    if is_tile_twin and player.tiles[cast(BaseTwinTile, tile_entity.tile).secondary_tile_id].has_stable:
                        for animal in storage_for_tile:
                            storage_for_tile[animal] *= 2
                else:
                    for effect in base_animal_storage_effects:
                        new_buckets_result: ResultLookup[Dict[ResourceTypeEnum, int]] = effect \
                            .get_animal_storage_buckets_for_tile(
                            player,
                            tile_entity)

                        if new_buckets_result:
                            new_buckets: Dict[ResourceTypeEnum, int] = new_buckets_result.value
                            self._update_storage_for_tile(
                                new_buckets,
                                storage_for_tile)

        return storage_for_tile

    def _update_storage_for_tile(
            self,
            new_buckets: Dict[ResourceTypeEnum, int],
            storage_for_tile: Dict[ResourceTypeEnum, int]) -> None:
        for animal in new_buckets:
            current_storage_for_animal: int = storage_for_tile[animal]
            new_storage_for_animal: int = new_buckets[animal]
            if new_storage_for_animal > current_storage_for_animal:
                storage_for_tile[animal] = new_storage_for_animal

    def _does_player_have_space_for_animals_with_dogs(
            self,
            player: BasePlayerRepository,
            player_animals: Dict[ResourceTypeEnum, int],
            animal_storage_buckets_without_dogs: Dict[int, Dict[ResourceTypeEnum, int]]) -> ResultLookup[bool]:
        success: bool = False

        positions_of_dogs: Iterable[Dict[int, Dict[ResourceTypeEnum, int]]] = self._get_animal_storage_buckets_for_player_accounting_for_dogs(
            player,
            animal_storage_buckets_without_dogs)

        for animal_storage_buckets_with_dogs in positions_of_dogs:
            if success:
                break

            evaluated_partitions: Iterable[Tuple[
                bool,
                Dict[int, Optional[ResourceTypeEnum]],
                Dict[ResourceTypeEnum, int],
                Dict[ResourceTypeEnum, int]
            ]] = self._resource_layout_checker \
                .check_resource_layout(
                animal_storage_buckets_with_dogs,
                player_animals)

            for (did_partition_store_all_animals, partition, remaining, excess) in evaluated_partitions:
                if did_partition_store_all_animals:
                    success = True
                    break

        if success:
            result = ResultLookup(True, True)
        else:
            result = ResultLookup(errors="Player does not have enough space to store all animals")
        return result

    def _get_animal_storage_buckets_for_player_accounting_for_dogs(
            self,
            player: BasePlayerRepository,
            animal_storage_buckets_without_dogs: Dict[int, Dict[ResourceTypeEnum, int]]) -> Iterable[Dict[int, Dict[ResourceTypeEnum, int]]]:
        ids_of_tiles_which_dogs_can_affect: List[int] = self._get_tiles_which_dogs_have_effect_on(player)
        number_of_tiles_which_dogs_can_affect: int = len(ids_of_tiles_which_dogs_can_affect)

        number_of_dogs: int = player.get_resources_of_type(ResourceTypeEnum.dog)

        for dog_partition in self._integer_partition_forge.generate_integer_partitions(number_of_dogs):
            if len(dog_partition) > number_of_tiles_which_dogs_can_affect:
                continue

            for permutation in self._integer_partition_permutation_forge.generate_permutation(
                    dog_partition,
                    number_of_tiles_which_dogs_can_affect):
                animal_storage_buckets_with_dogs: Dict[int, Dict[ResourceTypeEnum, int]] = animal_storage_buckets_without_dogs.copy()

                for i in range(number_of_tiles_which_dogs_can_affect):
                    tile_id: int = ids_of_tiles_which_dogs_can_affect[i]
                    number_of_dogs: int = permutation[i]

                    new_number_of_sheep_which_may_be_stored: int = number_of_dogs + 1

                    if tile_id in animal_storage_buckets_with_dogs:
                        current_number_of_sheep_which_may_be_stored: int = animal_storage_buckets_without_dogs[tile_id][ResourceTypeEnum.sheep]

                        if new_number_of_sheep_which_may_be_stored > current_number_of_sheep_which_may_be_stored:
                            animal_storage_buckets_with_dogs[tile_id][ResourceTypeEnum.sheep] = new_number_of_sheep_which_may_be_stored
                    else:
                        animal_storage_buckets_without_dogs[tile_id] = {
                            ResourceTypeEnum.sheep: new_number_of_sheep_which_may_be_stored,
                            ResourceTypeEnum.donkey: 0,
                            ResourceTypeEnum.boar: 0,
                            ResourceTypeEnum.cow: 0
                        }

                yield animal_storage_buckets_with_dogs

    def _get_tiles_which_dogs_have_effect_on(
            self,
            player: BasePlayerRepository) -> List[int]:
        result: List[int] = []
        for location, tile_entity in player.tiles.items():
            if tile_entity.tile_type in self._tile_types_dogs_can_effect:
                result.append(location)

        return result

    def new_turn_reset(self):
        self._animals_to_reproduce = None
