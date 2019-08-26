import math
from abc import ABC
from typing import Dict, Union, Type, List
from common.entities.player import Player
from common.entities.weapon import Weapon
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class BasePurchaseEffect(BaseEffect, ABC):
    """Abstract class for purchase effects"""

    def invoke(self, player: Player, target: Union[BaseTile, Weapon], current_price: Dict[ResourceTypeEnum, int]) \
            -> Dict[ResourceTypeEnum, int]:
        """Returns the new price of the target.

        :param player: The player who is attempting to purchase the item.
        :param target: The object whose price may be decreased. This cannot be null.
        :param current_price: The current price of the target. This cannot be null.
        :returns: A dictionary of resource type to int containing the new price. This will never be null.
        """
        raise NotImplementedError()


class DecreasePrice(BasePurchaseEffect):
    def __init__(self, subject: Union[Type[BaseTile], Type[Weapon]], decrease_by: Dict[ResourceTypeEnum, int]):
        """Decreases the price required to purchase something (either a tile, including pastures and stables or weapons)

        :param subject: The object which is effected by this discount. This cannot be null.
        :param decrease_by: The amount to decrease the cost by (down to a minimum of 0). This cannot be null.
        """
        if subject is None:
            raise ValueError("Subject cannot be none")
        if decrease_by is None:
            raise ValueError("Amount to decrease by cannot be null.")
        self._subject: Type = type(subject)
        self._decreaseBy: Dict[ResourceTypeEnum] = decrease_by
        BaseEffect.__init__(self)

    def invoke(
            self,
            player: Player,
            target: Union[BaseTile, Weapon],
            current_price: Dict[ResourceTypeEnum, int]) \
            -> Dict[ResourceTypeEnum, int]:
        """Returns the new price of the target.

        :param player: Unused.
        :param target: The object whose price may be decreased. This cannot be null.
        :param current_price: The current price of the target. This cannot be null.
        :returns: A dictionary of resource type to int containing the new price. This will never be null.
        """
        if target is None:
            raise ValueError("Target cannot be null")
        if current_price is None:
            raise ValueError("Current price cannot be null")

        if not isinstance(target, self._subject):
            return current_price

        result: Dict[ResourceTypeEnum, int] = {}

        for resource, decrease_cost_for_resource in self._decreaseBy.items():
            current_price_for_resource = current_price.get(resource, 0)

            if current_price_for_resource < decrease_cost_for_resource:
                current_price_for_resource = 0
            else:
                current_price_for_resource -= decrease_cost_for_resource

            result[resource] = current_price_for_resource
        return result

