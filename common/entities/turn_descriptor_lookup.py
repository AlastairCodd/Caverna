from typing import List

from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.constants import game_constants
from core.enums.harvest_type_enum import HarvestTypeEnum


class TurnDescriptorLookup(object):
    def __init__(
            self,
            cards: List[BaseCard],
            tiles: List[BaseTile],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> None:
        if cards is None:
            raise ValueError("Cards cannot be null")
        if len(cards) == 0:
            raise IndexError("Cards may not be empty")

        if tiles is None:
            raise ValueError("Tiles cannot be null")

        if turn_index < 0:
            raise IndexError(f"Turn index ({turn_index}) must be positive")

        if round_index < 0:
            raise IndexError(f"Round index ({round_index}) must be positive.")
        if round_index >= game_constants.number_of_rounds:
            raise IndexError(f"Round index ({round_index}) must be less than maximum number of rounds ({game_constants.number_of_rounds})")

        self._cards: List[BaseCard] = cards
        self._tiles: List[BaseTile] = tiles
        self._turn_index: int = turn_index
        self._round_index: int = round_index
        self._harvest_type: HarvestTypeEnum = harvest_type

    @property
    def cards(self) -> List[BaseCard]:
        return self._cards

    @property
    def tiles(self) -> List[BaseTile]:
        return self._tiles

    @property
    def turn_index(self) -> int:
        return self._turn_index

    @property
    def round_index(self) -> int:
        return self._round_index

    @property
    def harvest_type(self) -> HarvestTypeEnum:
        return self._harvest_type
