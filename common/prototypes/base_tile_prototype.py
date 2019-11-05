from buisness_logic.tiles.generic_tile import GenericTile
from core.baseClasses.base_prototype import BaseImmutablePrototype
from core.baseClasses.base_tile import BaseTile


class BaseTilePrototype(BaseImmutablePrototype[BaseTile]):
    def clone(self, source: BaseTile) -> BaseTile:
        if source is None:
            raise ValueError

        target = GenericTile(
            source.name,
            source.id,
            source.is_dwelling,
            source.base_points,
            source.cost,
            source.effects,
            source.colour)

        target.location = source.location

        return target
