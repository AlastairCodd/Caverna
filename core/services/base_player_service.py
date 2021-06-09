from abc import abstractmethod, ABCMeta
from typing import List, Dict, Tuple

from buisness_logic.effects.food_effects import BaseFoodEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.baseClasses.base_tile_container_default import BaseTileContainerDefault
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class BasePlayerService(BasePlayerRepository, metaclass=ABCMeta):
    def __init__(
            self,
            player_id: int,
            player_descriptor: str,
            turn_index: int,
            tile_container_default: BaseTileContainerDefault) -> None:
        BasePlayerRepository.__init__(
            self,
            player_id,
            player_descriptor,
            turn_index,
            tile_container_default)

    @abstractmethod
    def get_player_choice_conversions_to_perform(
            self,
            turn_descriptor: TurnDescriptorLookup) \
            -> List[Tuple[List[ResourceTypeEnum], int, List[ResourceTypeEnum]]]:
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_market_items_to_purchase(
            self,
            turn_descriptor: TurnDescriptorLookup) \
            -> ResultLookup[List[ResourceTypeEnum]]:
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_weapon_level(
            self,
            turn_descriptor: TurnDescriptorLookup) -> int:
        """Gets user choice for how strong a weapon to give to the current dwarf."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_animals_to_breed(
            self,
            animals_which_can_reproduce: List[ResourceTypeEnum],
            possible_number_of_animals_to_reproduce: int,
            turn_descriptor: TurnDescriptorLookup) \
            -> ResultLookup[List[ResourceTypeEnum]]:
        """Get user choice for which animals to breed.

        :param animals_which_can_reproduce: List of possible animals which can reproduce at the moment.
            This cannot be null.
        :param possible_number_of_animals_to_reproduce: Number of animals to choose.
            This will be in the range [0, len(animals_which_can_reproduce)].
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :returns: A list of animals which will be bred this turn. This will never be null, and length will match
            possible_number_of_animals_to_reproduce.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_use_dwarf_out_of_order(
            self,
            dwarves: List[Dwarf],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[bool]:
        """Gets user choice for whether or not to play a dwarf out of turn.

        :param dwarves: The dwarves the player has. This cannot be null, or empty.
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :returns: True if the player has chosen to play a dwarf out of turn, false if not."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_card_to_use(
            self,
            available_cards: List[BaseCard],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseCard]:
        """Gets user choice for which card to use.

        :param available_cards: The possible cards that may be chosen. This cannot be null, or empty.
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :returns: The card the player has chosen to activate."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_use_card_already_in_use(
            self,
            unused_available_cards: List[BaseCard],
            used_available_cards: List[BaseCard],
            amount_of_food_required: int,
            turn_descriptor: TurnDescriptorLookup) -> bool:
        """Gets user choice for which card to use.

        :param unused_available_cards: The possible cards that may be chosen, which may be used for free. This cannot be null, but may be empty.
        :param used_available_cards: The possible cards that may be chosen, which may be used at a cost. This cannot be null, or empty.
        :param amount_of_food_required: The amount of food that must be payed to use a card already in use. This may be zero.
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :returns: The card the player has chosen to activate."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_dwarf_to_use_out_of_order(
            self,
            dwarves: List[Dwarf],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[Dwarf]:
        """Gets user choice for which dwarf to play out of turn.

        :param dwarves: The dwarves the player has. This cannot be null, or empty.
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :returns: The dwarf the player has chosen to use out of turn."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_actions_to_use(
            self,
            available_action_choices: List[ActionChoiceLookup],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        """Gets user choice for which actions to take.

        :param available_action_choices: The possible action choices which may be chosen. This cannot be null, or empty.
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :returns: The action choice the player has chosen to take."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_tile_to_build(
            self,
            possible_tiles: List[BaseTile],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseTile]:
        """Gets user choice for which tile to build.

        :param possible_tiles: The possible tiles which may be built. This cannot be null, or empty.
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :returns: The tile the player has chosen to build. This will never be null."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_expedition_reward(
            self,
            possible_expedition_rewards: List[BaseAction],
            expedition_level: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseAction]]:
        """Gets user choice for which expedition rewards to use.

        :param possible_expedition_rewards: The possible expedition rewards that may be chosen, given the level of the dwarf. This cannot be null, or empty.
        :param expedition_level: The number of rewards the player must take. This must be positive.
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :returns: The expedition rewards the player has chosen to claim. This will never be null."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_location_to_build(
            self,
            tile: BaseTile,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[int]:
        """Gets user choice for location to place the given tile.

        :param tile: The tile to be placed. This cannot be null.
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :returns: The location that the player has decided to place this tile. This will never be null."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_location_to_build_twin(
            self,
            tile_type: TileTypeEnum,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[TileTwinPlacementLookup]:
        """Gets user choice for location to place the given twin tile.

        :param tile_type: The type of the twin tile to be placed. This cannot be null.
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :returns: The location and direction that the player has decided to place this tile. This will never be null."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_location_to_build_stable(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[int]:
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_effects_to_use_for_cost_discount(
            self,
            tile_cost: Dict[ResourceTypeEnum, int],
            turn_descriptor: TurnDescriptorLookup) -> Dict[BaseTilePurchaseEffect, int]:
        pass

    @abstractmethod
    def get_player_choice_use_harvest_action_instead_of_breeding(
            self,
            turn_descriptor: TurnDescriptorLookup) -> bool:
        pass

    @abstractmethod
    def get_player_choice_effect_to_use_for_feeding_dwarves(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseFoodEffect]]:
        pass

    @abstractmethod
    def get_player_choice_locations_to_sow(
            self,
            number_of_resources_to_sow: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[int]]:
        pass

    @abstractmethod
    def get_player_choice_resources_to_sow(
            self,
            number_of_resources_to_sow: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[ResourceTypeEnum]]:
        pass
