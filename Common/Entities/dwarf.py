from Common.Entities.weapon import Weapon

class Dwarf(object):
	_isAdult: bool
	_weapon: Weapon
	_currentCard = None
	
	def __init__(self, isAdult: bool = False):
		self._isAdult = isAdult
		self._weapon = None
	
	def IsAdult(self) -> bool:
		return self._isAdult
			
	def SetIsAdult(self, isAdult: bool) -> bool:
		self._isAdult = isAdult
		return self._isAdult
	
	def GiveWeapon(self, weapon: Weapon):
		if self._weapon is not None:
			raise ValueError("dwarf already has a weapon")
		
		self._weapon = weapon
		
	def GetWeapon(self) -> Weapon:
		return self._weapon
	
	def SetActive(self, currentCard):
		if currentCard is None:
			raise ValueError("current card must not be none")
	
		if self._currentCard is not None:
			raise ValueError("already active")
		
		self._currentCard = currentCard
		
	def ClearActiveCard(self):
		self._currentCard = None
		
	def GetIsActive(self) -> bool:
		isActive = self._currentCard is None
		return isActive