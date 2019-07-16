from Common.Entities.dwarf import Dwarf

class DwarfAgeService(object):

	def AgeUpDwarf(self, dwarf: Dwarf) -> bool:
		if not dwarf.IsAdult():
			return False

		dwarf.SetIsAdult(True)
		return True
	
	def GetFoodRequiredForDwarf(self, dwarf: Dwarf) -> int:
		if dwarf None:
			raise ValueException("dwarf must not be none")
		
		if dwarf.IsAdult():
			return 2
		else:
			return 1