from typing import Dict

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum


class StartingPlayerRubyCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Starting Player", card_ids.StartingPlayerRubyCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(False),
                Conditional(
                    ActionCombinationEnum.AndThen,
                    become_starting_player_action.BecomeStartingPlayerAction(),
                    receive_action.ReceiveAction({ResourceTypeEnum.ruby: 1}))))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.food, 1)

        return self.resources


class StartingPlayerOreCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Starting Player", card_ids.StartingPlayerOreCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(False),
                Conditional(
                    ActionCombinationEnum.AndThen,
                    become_starting_player_action.BecomeStartingPlayerAction(),
                    receive_action.ReceiveAction({ResourceTypeEnum.ore: 2}))))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.food, 1)

        return self.resources
