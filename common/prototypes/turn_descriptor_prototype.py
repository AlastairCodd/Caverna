from typing import List

from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.prototypes.base_tile_prototype import BaseTilePrototype
from common.prototypes.card_prototype import CardPrototype
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_prototype import BaseImmutablePrototype
from core.baseClasses.base_tile import BaseTile


class TurnDescriptorPrototype(BaseImmutablePrototype[TurnDescriptorLookup]):
    def __init__(self) -> None:
        self._card_prototype: BaseImmutablePrototype[BaseCard] = CardPrototype()
        self._tile_prototype: BaseImmutablePrototype[BaseTile] = BaseTilePrototype()

    def clone(self, source: TurnDescriptorLookup) -> TurnDescriptorLookup:
        if source is None:
            raise ValueError("Source may not be None")

        cards: List[BaseCard] = self._card_prototype.clone_range(source.cards)
        tiles: List[BaseTile] = self._tile_prototype.clone_range(source.tiles)

        result: TurnDescriptorLookup = TurnDescriptorLookup(
            cards,
            tiles,
            source.turn_index,
            source.round_index,
            source.harvest_type)

        return result
