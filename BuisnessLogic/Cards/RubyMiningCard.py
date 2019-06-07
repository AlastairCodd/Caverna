from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class RubyMiningCard(BaseCard, ResourceContainer):
	
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
			
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		newResources = {ResourceTypeEnum.ruby: 1} if self.HasResources() else {ResourceTypeEnum.ruby: 2}
		self.GiveResources(newResources)
		
		return self.GetResources()
