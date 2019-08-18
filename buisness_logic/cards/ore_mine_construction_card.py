from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class OreMineConstructionCard(BaseCard):
	
	def __init__(self):
		self._name = "Ore Mine Construction"
		self._id = 22
		self._level = 1
		self._actions = Combination(
			ActionCombinationEnum.AndThenOr,
			Combination(
				ActionCombinationEnum.AndThen,
				placeATileAction.PlaceATileAction( TileTypeEnum.oreMineDeepTunnelTwin ),
				receiveAction.ReceiveAction( { ResourceTypeEnum.ore: 3 } ) ),
			goOnAnExpeditionAction.GoOnAnExpeditionAction( 3 ) )