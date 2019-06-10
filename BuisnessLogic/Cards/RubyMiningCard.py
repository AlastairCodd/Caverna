from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class RubyMiningCard(BaseCard, ActiveResourceContainer):
	
	def __init__(self):
		self._name = "Ruby Mining"
		self._id = 33
		self._level = 4
		
		conditional = lambda person, card: 
			if person is None:
				raise ValueError("ruby mining card conditional person")
			tiles = person.GetTiles()
			return False
		
		self._actions = Combination(
			ActionCombinationEnum.AndThenOr,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
			receiveConditionallyAction.ReceiveConditionallyAction( conditional ) )
				
		super(RubyMiningCard, self).__init__()
			
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		if self.HasResources():
			newResources = {ResourceTypeEnum.ruby: 1} 
		else:
			newResources = {ResourceTypeEnum.ruby: 2} 
		self.GiveResources(newResources)
		
		return self.GetResources()
