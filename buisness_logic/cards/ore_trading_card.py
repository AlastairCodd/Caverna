from buisness_logic.actions import pay_action, receive_action
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ActionCombinationEnum, ResourceTypeEnum


class OreTradingCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Ore Trading", 32, 4,
            actions=Conditional(
                ActionCombinationEnum.AndOr,
                Conditional(
                    ActionCombinationEnum.AndThen,
                    pay_action.PayAction({ResourceTypeEnum.ore: 2}),
                    receive_action.ReceiveAction({ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 1})),
                Conditional(
                    ActionCombinationEnum.AndOr,
                    Conditional(
                        ActionCombinationEnum.AndThen,
                        pay_action.PayAction({ResourceTypeEnum.ore: 2}),
                        receive_action.ReceiveAction({ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 1})),
                    Conditional(
                        ActionCombinationEnum.AndThen,
                        pay_action.PayAction({ResourceTypeEnum.ore: 2}),
                        receive_action.ReceiveAction({ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 1})))))
