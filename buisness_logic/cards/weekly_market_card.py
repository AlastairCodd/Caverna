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
                receive_action.ReceiveAction({ResourceTypeEnum.coin: 4}),
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
                                    pay_action.PayAction({ResourceTypeEnum.coin: 2}),
                                    receive_action.ReceiveAction({ResourceTypeEnum.dog: 1})
                                ),
                                Conditional(  # sheep
                                    ActionCombinationEnum.AndThen,
                                    pay_action.PayAction({ResourceTypeEnum.coin: 1}),
                                    receive_action.ReceiveAction({ResourceTypeEnum.sheep: 1})
                                )
                            ),
                            Conditional(  # 2
                                ActionCombinationEnum.AndOr,
                                Conditional(  # donkey
                                    ActionCombinationEnum.AndThen,
                                    pay_action.PayAction({ResourceTypeEnum.coin: 1}),
                                    receive_action.ReceiveAction({ResourceTypeEnum.donkey: 1})
                                ),
                                Conditional(  # boar
                                    ActionCombinationEnum.AndThen,
                                    pay_action.PayAction({ResourceTypeEnum.coin: 2}),
                                    receive_action.ReceiveAction({ResourceTypeEnum.boar: 1})
                                )
                            )
                        ),
                        Conditional(  # 7
                            ActionCombinationEnum.AndOr,
                            Conditional(  # 3
                                ActionCombinationEnum.AndOr,
                                Conditional(  # cow
                                    ActionCombinationEnum.AndThen,
                                    pay_action.PayAction({ResourceTypeEnum.coin: 3}),
                                    receive_action.ReceiveAction({ResourceTypeEnum.cow: 1})
                                ),
                                Conditional(  # wood
                                    ActionCombinationEnum.AndThen,
                                    pay_action.PayAction({ResourceTypeEnum.coin: 1}),
                                    receive_action.ReceiveAction({ResourceTypeEnum.wood: 1})
                                )
                            ),
                            Conditional(  # 4
                                ActionCombinationEnum.AndOr,
                                Conditional(  # stone
                                    ActionCombinationEnum.AndThen,
                                    pay_action.PayAction({ResourceTypeEnum.coin: 1}),
                                    receive_action.ReceiveAction({ResourceTypeEnum.stone: 1})
                                ),
                                Conditional(  # ore
                                    ActionCombinationEnum.AndThen,
                                    pay_action.PayAction({ResourceTypeEnum.coin: 2}),
                                    receive_action.ReceiveAction({ResourceTypeEnum.ore: 1})
                                )
                            )
                        ),
                    ),
                    Conditional(  # 5
                        ActionCombinationEnum.AndOr,
                        Conditional(  # grain
                            ActionCombinationEnum.AndThen,
                            pay_action.PayAction({ResourceTypeEnum.coin: 1}),
                            receive_action.ReceiveAction({ResourceTypeEnum.grain: 1})
                        ),
                        Conditional(  # veg
                            ActionCombinationEnum.AndThen,
                            pay_action.PayAction({ResourceTypeEnum.coin: 2}),
                            receive_action.ReceiveAction({ResourceTypeEnum.veg: 1})
                        )
                    )
                )))
