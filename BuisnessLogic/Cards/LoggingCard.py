from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Common.Entities.multiconditional import Conditional
from BuisnessLogic.Actions.takeAccumulatedItemsAction import TakeAccumulatedItemsAction
from BuisnessLogic.Actions.goOnAnExpeditionAction import GoOnAnExpeditionAction

class LoggingCard(BaseCard):
	
	def __init__(self):
		self._name = "Logging"
		self._id = 13
		self._level = -1
		self._actions = Conditional(
			ActionCombinationEnum.AndThenOr,
			TakeAccumulatedItemsAction(),
			GoOnAnExpeditionAction(1) )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( ResourceTypeEnum.wood, 3 )
		
		return self.GetResources()
