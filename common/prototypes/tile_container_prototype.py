from typing import Optional

from common.defaults.tile_container_default import TileContainerDefault
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
        target = TileContainer(TileContainerDefault(), source.height, source.width)

        self.assign(source, target)
        return target

    def assign(self, source: TileContainer, target: TileContainer) -> None:
        # TODO: Testttt
        if source is None:
            raise ValueError("Source may not be None")
        if target is None:
            raise ValueError("Target may not be None")

        if source.height != target.height:
            raise ValueError
        if source.width != target.width:
            raise ValueError

        for i in range(source.tile_count):
            source_tile: Optional[BaseTile] = source.get_specific_tile_at_location(i)
            if source_tile is None:
                continue
            target_tile = target.get_specific_tile_at_location(i)

            # if the new target is empty and the source is not, set the new one
            if target_tile is None:
                new_tile_clone: BaseTile = self._tile_prototype.clone(source_tile)
                target.tiles[i].set_tile(new_tile_clone)
                continue

            # specific case for transparent tile
            if source_tile.id == target_tile.id == -1:
                # could check that the effects are equal but that seems overkill
                #    you (the player) can't do anything to create a tile with id
                #    of -1 (as those are only transparent tiles (inb4...)), so
                #    this should be sufficient
                continue

            # TODO: other specific cases?

            new_tile_clone: BaseTile = self._tile_prototype.clone(source_tile)
            target.tiles[i].set_tile(new_tile_clone)
