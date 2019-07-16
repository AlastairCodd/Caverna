from core.enums.cavernaEnums import ActionCombinationEnum

class Combination(object):
	
	def __init__(self, type: ActionCombinationEnum, combine1, combine2):
		if combine1 is None:
			raise ValueError("combine1")
		if combine2 is None:
			raise ValueError("combine2")
			
		self._combine1 = combine1
		self._combine2 = combine2
		self._type = type