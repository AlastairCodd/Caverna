from typing import Dict

from buisness_logic.actions import placeATileAction, takeAccumulatedItemsAction
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum


class SheepFarmingCard(BaseCard, ResourceContainer):
    def __init__(self):
        BaseCard.__init__(
            self, "Sheep Farming", 24, 2,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                Conditional(
                    ActionCombinationEnum.AndOr,
                    Conditional(
                        ActionCombinationEnum.AndOr,
                        placeATileAction.PlaceATileAction(TileTypeEnum.pasture),
                        placeATileAction.PlaceATileAction(TileTypeEnum.pastureTwin)),
                    placeATileAction.PlaceAStableAction()),
                takeAccumulatedItemsAction.TakeAccumulatedItemsAction()))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.sheep, 1)

        return self.resources
