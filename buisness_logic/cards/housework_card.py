from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class HouseworkCard(BaseCard):
	
	def __init__(self):
		self._name = "Housework"
		self._id = 8
		self._level = -1
		self._actions = Combination( 
			ActionCombinationEnum.AndOr,
			receiveAction.ReceiveAction( {ResourceTypeEnum.dog: 1} ),
			placeATileAction.PlaceATileAction( TileTypeEnum.furnishedCavern ) )