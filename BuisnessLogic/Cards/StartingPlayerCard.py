from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Common.Entities.multiconditional import Conditional
from BuisnessLogic.Actions.takeAccumulatedItemsAction import TakeAccumulatedItemsAction
from BuisnessLogic.Actions.receiveAction import ReceiveAction
from BuisnessLogic.Actions.becomeStartingPlayerAction import BecomeStartingPlayerAction

class StartingPlayerCard(BaseCard):
	
	def __init__(self):
		self._name = "Starting Player"
		self._id = 17
		self._level = -1
		self._actions = Conditional(
			ActionCombinationEnum.AndThen,
			TakeAccumulatedItems(),
			Conditional(
				ActionCombinationEnum.AndThen,
				BecomeStartingPlayerAction(),
				ReceiveAction( {ResourceTypeEnum.ruby, 1} ) ) )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( ResourceTypeEnum.food, 1 )
		
		return self.GetResources()
