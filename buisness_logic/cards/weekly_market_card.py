from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from buisness_logic.actions import *


class WeeklyMarketCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Weekly Market", 20,
            actions=Conditional(
                ActionCombinationEnum.AndOr,
                receiveAction.ReceiveAction({ResourceTypeEnum.coin: 4}),
                Conditional(  # 9
                    ActionCombinationEnum.AndOr,
                    Conditional(  # 8
                        ActionCombinationEnum.AndOr,
                        Conditional(  # 6
                            ActionCombinationEnum.AndOr,
                            Conditional(  # 1
                                ActionCombinationEnum.AndOr,
                                Conditional(  # dog
                                    ActionCombinationEnum.AndThen,
                                    payAction.PayAction({ResourceTypeEnum.coin: 2}),
                                    receiveAction.ReceiveAction({ResourceTypeEnum.dog: 1})
                                ),
                                Conditional(  # sheep
                                    ActionCombinationEnum.AndThen,
                                    payAction.PayAction({ResourceTypeEnum.coin: 1}),
                                    receiveAction.ReceiveAction({ResourceTypeEnum.sheep: 1})
                                )
                            ),
                            Conditional(  # 2
                                ActionCombinationEnum.AndOr,
                                Conditional(  # donkey
                                    ActionCombinationEnum.AndThen,
                                    payAction.PayAction({ResourceTypeEnum.coin: 1}),
                                    receiveAction.ReceiveAction({ResourceTypeEnum.donkey: 1})
                                ),
                                Conditional(  # boar
                                    ActionCombinationEnum.AndThen,
                                    payAction.PayAction({ResourceTypeEnum.coin: 2}),
                                    receiveAction.ReceiveAction({ResourceTypeEnum.boar: 1})
                                )
                            )
                        ),
                        Conditional(  # 7
                            ActionCombinationEnum.AndOr,
                            Conditional(  # 3
                                ActionCombinationEnum.AndOr,
                                Conditional(  # cow
                                    ActionCombinationEnum.AndThen,
                                    payAction.PayAction({ResourceTypeEnum.coin: 3}),
                                    receiveAction.ReceiveAction({ResourceTypeEnum.cow: 1})
                                ),
                                Conditional(  # wood
                                    ActionCombinationEnum.AndThen,
                                    payAction.PayAction({ResourceTypeEnum.coin: 1}),
                                    receiveAction.ReceiveAction({ResourceTypeEnum.wood: 1})
                                )
                            ),
                            Conditional(  # 4
                                ActionCombinationEnum.AndOr,
                                Conditional(  # stone
                                    ActionCombinationEnum.AndThen,
                                    payAction.PayAction({ResourceTypeEnum.coin: 1}),
                                    receiveAction.ReceiveAction({ResourceTypeEnum.stone: 1})
                                ),
                                Conditional(  # ore
                                    ActionCombinationEnum.AndThen,
                                    payAction.PayAction({ResourceTypeEnum.coin: 2}),
                                    receiveAction.ReceiveAction({ResourceTypeEnum.ore: 1})
                                )
                            )
                        ),
                    ),
                    Conditional(  # 5
                        ActionCombinationEnum.AndOr,
                        Conditional(  # grain
                            ActionCombinationEnum.AndThen,
                            payAction.PayAction({ResourceTypeEnum.coin: 1}),
                            receiveAction.ReceiveAction({ResourceTypeEnum.grain: 1})
                        ),
                        Conditional(  # veg
                            ActionCombinationEnum.AndThen,
                            payAction.PayAction({ResourceTypeEnum.coin: 2}),
                            receiveAction.ReceiveAction({ResourceTypeEnum.veg: 1})
                        )
                    )
                )))
