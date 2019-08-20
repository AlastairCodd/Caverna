from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class OreMiningCard(BaseCard, ActiveResourceContainer):
	
	def __init__(self):
		self._name = "Ore Mining"
		self._id = 14
		self._level = -1
		
		conditional = lambda person, card : False
			#if person is None:
				#raise ValueError("ruby mining card conditional person")
			#tiles = person.GetTiles()
			#return False
		
		self._actions = Combination(
			ActionCombinationEnum.AndThenOr,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
			receiveConditionallyAction.ReceiveConditionallyAction( 
				conditional, 
				{ ResourceTypeEnum.ore: 1 } ) )
				
		super(OreMiningCard, self).__init__()
			
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		if self.HasResources():
			newResources = {ResourceTypeEnum.ore: 2} 
		else:
			newResources = {ResourceTypeEnum.ore: 3} 
		self.GiveResources(newResources)
		
		return self.GetResources()
