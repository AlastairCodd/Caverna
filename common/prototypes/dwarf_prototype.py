from common.entities.dwarf import Dwarf
from core.baseClasses.base_prototype import BasePrototype


class DwarfPrototype(BasePrototype[Dwarf]):
    def clone(self, source: Dwarf) -> Dwarf:
        if source is None:
            raise ValueError

        target: Dwarf = Dwarf()
        self.assign(source, target)
        return target

    def assign(self, source: Dwarf, target: Dwarf) -> None:
        if source is None:
            raise ValueError
        if target is None:
            raise ValueError

        if source.is_adult:
            target.make_adult()
        elif target.is_adult:
            raise ValueError
