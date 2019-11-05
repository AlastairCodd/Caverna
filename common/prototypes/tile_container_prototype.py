from common.prototypes.base_tile_prototype import BaseTilePrototype
from core.baseClasses.base_prototype import BasePrototype, BaseImmutablePrototype
from core.baseClasses.base_tile import BaseTile
from core.containers.tile_container import TileContainer


class TileContainerPrototype(BasePrototype[TileContainer]):
    def __init__(self):
        self._tile_prototype: BaseImmutablePrototype[BaseTile] = BaseTilePrototype()

    def clone(self, source: TileContainer) -> TileContainer:
        if source is None:
            raise ValueError
        target = TileContainer(source.height, source.width)

        self.assign(source, target)
        return target

    def assign(self, source: TileContainer, target: TileContainer) -> None:
        if source is None:
            raise ValueError
        if target is None:
            raise ValueError

        if source.height != target.height:
            raise ValueError
        if source.width != target.width:
            raise ValueError

        for i in range(source.tile_count):
            source_tile: BaseTile = source.get_tile_at_location(i)
            new_tile_clone: BaseTile = self._tile_prototype.clone(source_tile)
            target.place_tile(new_tile_clone, i)

