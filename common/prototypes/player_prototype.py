from common.entities.player import Player
from common.prototypes.dwarf_prototype import DwarfPrototype
from common.prototypes.resource_container_prototype import ResourceContainerPrototype
from core.baseClasses.base_prototype import BasePrototype


class PlayerPrototype(BasePrototype[Player]):
    def __init__(self):
        self._dwarf_prototype: DwarfPrototype = DwarfPrototype()
        self._resource_container_prototype: ResourceContainerPrototype = ResourceContainerPrototype()

    def clone(self, source: Player) -> Player:
        if source is None:
            raise ValueError

        target = Player(source.id, source.turn_index)
        self.assign(source, target)
        return target

    def assign(self, source: Player, target: Player) -> None:
        if source is None:
            raise ValueError
        if target is None:
            raise ValueError

        target.dwarves.clear()
        for dwarf in source.dwarves:
            target.dwarves.append(self._dwarf_prototype.clone(dwarf))