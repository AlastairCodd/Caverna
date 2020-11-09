from common.entities.dwarf import Dwarf


class DwarfAgeService(object):
    # TODO: Use or delete
    def age_up_dwarf(self, dwarf: Dwarf) -> bool:
        if not dwarf.is_adult:
            return False

        dwarf.make_adult()
        return True

    def get_food_required_for_dwarf(self, dwarf: Dwarf) -> int:
        if dwarf is None:
            raise ValueError("dwarf must not be none")

        if dwarf.is_adult:
            return 2
        else:
            return 1
