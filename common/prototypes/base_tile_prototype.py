from buisness_logic.tiles.generic_tile import GenericTile, GenericSpecificTile
from core.baseClasses.base_prototype import BaseImmutablePrototype
from core.baseClasses.base_tile import BaseTile, BaseSpecificTile


class BaseTilePrototype(BaseImmutablePrototype[BaseTile]):
    def clone(
            self,
            source: BaseTile) -> BaseTile:
        if source is None:
            raise ValueError("Source may not be None")

        target: BaseTile

        if isinstance(source, BaseSpecificTile):
            target = GenericSpecificTile(
                source.name,
                source.id,
                source.tile_type,
                source.base_points,
                source.cost,
                source.effects,
                source.colour)
        else:
            target = GenericTile(
                source.name,
                source.id,
                source.tile_type,
                source.base_points,
                source.cost,
                source.effects)

        target.location = source.location

        return target
