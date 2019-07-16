from common.entities.dwarf import Dwarf

class DwarfAgeService(object):

	def age_up_dwarf(self, dwarf: Dwarf) -> bool:
		if not dwarf.IsAdult():
			return False

		dwarf.SetIsAdult(True)
		return True
	
	def get_food_required_for_dwarf(self, dwarf: Dwarf) -> int:
		if dwarf None:
			raise ValueException("dwarf must not be none")
		
		if dwarf.IsAdult():
			return 2
		else:
			return 1