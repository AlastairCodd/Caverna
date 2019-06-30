from typing import Iterable, Dict
from Common.Entities.dwarf import Dwarf
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ResourceContainer

class Player(ResourceContainer):
	_id: int
	_turnIndex: int
	_dwarves: Iterable[Dwarf]
	_resources: Dict[ResourceTypeEnum, int]

	def __init__(
		self, 
		id: int, 
		turnIndex: int):
		
		self._id = id
		self._turnIndex = turnIndex
		
		self._dwarves = [
			Dwarf(True),
			Dwarf(True),
		]
	
    def SetTurnIndex(self, turnIndex: int):
        
    
	def GiveBabyDwarf(self):
		babyDwarf: Dwarf = Dwarf()
		
		self._dwarves.append(babyDwarf)
		
	def GetDwarves(self) -> Iterable[Dwarf]:
		return self._dwarves
		
	def GetPlayerResponse(self, action)
		"""Gets a player response for the given action. 
		Implementation left to implementing class -- either from user input, or from analysis of the action value function
		
		Returns relevant information to allow the calling action to change the player or board state based in accordance with the action"""
		raise NotImplementedError()
		
		