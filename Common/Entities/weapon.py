class Weapon(object):
	_level: int

	def __init__(self, level:int):
		if level < 1 or level > 8:
			raise ValueError("level at creation must be between 1 and 8")
		self._level = level
	
	def IncreaseLevel(self) -> int:
		self._level += 1
		return self._level
		
	def GetLevel(self) -> int:
		return self._level