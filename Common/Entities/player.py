from abc import abstractmethod, ABC
from typing import Iterable, List, Dict, Union
from common.entities.dwarf import Dwarf
from common.entities.weapon import Weapon
from core.baseClasses.base_tile import BaseTile
from core.containers.resource_container import ResourceContainer
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ResourceTypeEnum


class Player(TileContainer, ResourceContainer, ABC):

    def __init__(self, player_id: int, turn_index: int):
        self._id: int = player_id
        self._turnIndex: int = turn_index

        self._dwarves: List[Dwarf] = [Dwarf(True), Dwarf(True)]

        TileContainer.__init__(self)
        ResourceContainer.__init__(self)

    @property
    def id(self) -> int:
        return self._id

    @property
    def dwarves(self) -> List[Dwarf]:
        return list(self._dwarves)

    @property
    def turn_index(self) -> int:
        return self._turnIndex

    def set_turn_index(self, turn_index: int):
        self._turnIndex = turn_index

    def give_baby_dwarf(self):
        baby_dwarf: Dwarf = Dwarf()

        self._dwarves.append(baby_dwarf)

    @property
    def can_take_move(self) -> bool:
        """Determines whether this player can still make a move this turn"""
        is_dwarf_active: Iterable[bool] = map(lambda x: not x.is_active(), self._dwarves)
        return any(is_dwarf_active)

    def start_new_turn(self):
        for dwarf in self._dwarves:
            dwarf.make_adult()

    def get_player_choice(self, action):
        """Gets a player response for the given action.
        Implementation left to implementing class -- either from user input, or
            from analysis of the action value function

        Returns relevant information to allow the calling action to change
            the player or board state based in accordance with the action"""
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_market_action(
            self,
            possible_items_and_costs: Dict[ResourceTypeEnum, int]) \
            -> List[ResourceTypeEnum]:
        raise NotImplementedError()

    @abstractmethod
    def get_player_choice_weapon_level(self) -> int:
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
