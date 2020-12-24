from abc import abstractmethod, ABCMeta
from typing import List, Dict, Union, Optional

from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_unknown_placement_lookup import TileUnknownPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.entities.weapon import Weapon
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.baseClasses.base_tile_container_default import BaseTileContainerDefault
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class BasePlayerService(BasePlayerRepository, metaclass=ABCMeta):
    def __init__(
            self,
            player_id: int,
            turn_index: int,
            tile_container_default: BaseTileContainerDefault) -> None:
        BasePlayerRepository.__init__(self, player_id, turn_index, tile_container_default)

    @abstractmethod
    def get_player_choice_market_action(
            self,
            possible_items_and_costs: Dict[ResourceTypeEnum, int]) \
            -> List[ResourceTypeEnum]:
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_weapon_level(
            self,
            turn_descriptor: TurnDescriptorLookup) -> int:
        """Gets user choice for how strong a weapon to give to the current dwarf."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_breed_animals(
            self,
            animals_which_can_reproduce: List[ResourceTypeEnum],
            possible_number_of_animals_to_reproduce: int) \
            -> List[ResourceTypeEnum]:
        """Get user choice for which animals to breed.

        :param animals_which_can_reproduce: List of possible animals which can reproduce at the moment.
            This cannot be null.
        :param possible_number_of_animals_to_reproduce: Number of animals to choose.
            This will be in the range [0, len(animals_which_can_reproduce)].
        :returns: A list of animals which will be bred this turn. This will never be null, and length will match
            possible_number_of_animals_to_reproduce.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_discount(
            self,
            possible_prices: List[Dict[ResourceTypeEnum, int]],
            target: Union[BaseTile, Weapon]) \
            -> Dict[ResourceTypeEnum, int]:
        """Gets user choice for which discount level to apply.

        :param possible_prices: A list of possible costs for some item (either a tile or a weapon). This cannot be null.
        :param target: The item which is to be purchased. This cannot be null.
        :returns: The chosen cost of the item. This will never be null, and will be an element of possible_prices.
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
            turn_descriptor: TurnDescriptorLookup,
            secondary_tile: Optional[BaseTile] = None) -> ResultLookup[TileUnknownPlacementLookup]:
        """Gets user choice for location to place the given tile.

        :param tile: The tile to be placed. This cannot be null.
        :param turn_descriptor: The description of game state. This cannot be null, or empty.
        :param secondary_tile: The secondary tile to be placed, if the specified tile type is twin. This cannot be null, or empty.
        :returns: The location (and direction, if the tile is a twin-tile) that the place has decided to place this tile. This will never be null."""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_effects_to_use_for_cost_discount(
            self,
            specific_tile: BaseTile,
            turn_descriptor: TurnDescriptorLookup,
            secondary_tile: Optional[BaseTile] = None) -> Dict[BaseTilePurchaseEffect, int]:
        pass
