from typing import List

from buisness_logic.tiles.generic_tile import GenericTile, GenericSpecificTile
from common.prototypes.effect_prototype import EffectPrototype
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_prototype import BaseImmutablePrototype
from core.baseClasses.base_tile import BaseTile, BaseSpecificTile


class BaseTilePrototype(BaseImmutablePrototype[BaseTile]):
    def __init__(self) -> None:
        self._effect_prototype: BaseImmutablePrototype[BaseEffect] = EffectPrototype()

    def clone(
            self,
            source: BaseTile) -> BaseTile:
        if source is None:
            raise ValueError("Source may not be None")

        target: BaseTile

        effects: List[BaseEffect] = self._effect_prototype.clone_range(source.effects)

        if isinstance(source, BaseSpecificTile):
            target = GenericSpecificTile(
                source.name,
                source.id,
                source.tile_type,
                source.base_points,
                source.cost,
                effects,
                source.colour)
        else:
            target = GenericTile(
                source.name,
                source.id,
                source.tile_type,
                source.base_points,
                source.cost,
                effects)

        return target
