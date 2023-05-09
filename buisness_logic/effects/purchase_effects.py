from abc import ABCMeta, abstractmethod
from typing import Dict

from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum


class BaseTilePurchaseEffect(BaseEffect, metaclass=ABCMeta):
    """Abstract class for effects that effect the tile purchase cost"""
    def __init__(self, can_be_used_only_once: bool = True) -> None:
        self._can_be_used_only_once = can_be_used_only_once
        BaseEffect.__init__(self, False)

    @property
    def can_be_used_only_once(self) -> bool:
        return self._can_be_used_only_once

    @abstractmethod
    def invoke(
            self,
            current_price: Dict[ResourceTypeEnum, int]) -> Dict[ResourceTypeEnum, int]:
        """Returns the new price of the target.

        :param current_price: The current price of the target. This cannot be null.
        :returns: A dictionary containing the the new price. This will never be null.
        """
        raise NotImplementedError()


class DecreasePriceOfTileEffect(BaseTilePurchaseEffect):
    def __init__(
            self,
            decrease_by: Dict[ResourceTypeEnum, int]):
        """Decreases the price required to purchase a tile.

        :param decrease_by: The amount to decrease the cost by (down to a minimum of 0). This cannot be null.
        """
        if decrease_by is None:
            raise ValueError("Amount to decrease by cannot be null.")
        self._decreaseBy: Dict[ResourceTypeEnum] = decrease_by
        BaseTilePurchaseEffect.__init__(self, True)

    def invoke(
            self,
            current_price: Dict[ResourceTypeEnum, int]) -> Dict[ResourceTypeEnum, int]:
        """Returns the new price of the target.

        :param current_price: The current price of the target. This cannot be null.
        :returns: A dictionary of resource type to int containing the new price. This will never be null.
        """
        if current_price is None:
            raise ValueError("Current price cannot be null")

        new_price: Dict[ResourceTypeEnum, int] = dict(current_price)

        for resource in self._decreaseBy:
            current_price_for_resource = new_price.get(resource, 0)
            current_price_for_resource -= self._decreaseBy[resource]

            new_price[resource] = current_price_for_resource

        return new_price


class AllowSubstitutionForPurchaseEffect(BaseTilePurchaseEffect):
    def __init__(
            self,
            substitute_for: Dict[ResourceTypeEnum, int],
            substitute_with: Dict[ResourceTypeEnum, int]):
        """Generates alternative costs by substituting x for y

        :param substitute_for: The portion of the price to be removed. This cannot be null.
        :param substitute_with: The portion of the price to be added. This cannot be null.
        """
        if substitute_for is None:
            raise ValueError("Substitute for cannot be null")
        if substitute_with is None:
            raise ValueError("Substitute with cannot be null")
        self._substitute_for: Dict[ResourceTypeEnum, int] = substitute_for
        self._substitute_with: Dict[ResourceTypeEnum, int] = substitute_with

        BaseTilePurchaseEffect.__init__(self, False)

    def invoke(
            self,
            current_price: Dict[ResourceTypeEnum, int]) -> Dict[ResourceTypeEnum, int]:
        """Returns the new price of the target. This may have negative costs -- it is up to the consumer to check this.

        :param current_price: The current price of the target. This cannot be null.
        :returns: A dictionary of resource type to int containing the new price. This will never be null.
        """
        if current_price is None:
            raise ValueError("Current price cannot be null")

        new_price: Dict[ResourceTypeEnum, int] = dict(current_price)

        is_contained: bool = True

        for resource in self._substitute_for:
            if resource in new_price and new_price[resource] >= self._substitute_for[resource]:
                new_price[resource] -= self._substitute_for[resource]
            else:
                is_contained = False

        if is_contained:
            for resource in self._substitute_with:
                if resource not in new_price:
                    new_price[resource] = 0
                new_price[resource] += self._substitute_with[resource]
        else:
            new_price = current_price

        return new_price

    def __str__(self) -> str:
        return __format__(self, "")

    def __format__(self, format_spec):
        text = [("", "Allow ")]
        for (i, (resource, amount)) in enumerate(self._substitute_for.items()):
            text.append(("class:count", str(amount)))
            text.append(("", " "))
            text.append(("class:resource", resource.name))
            if amount != 1:
                text.append(("class:resource", "s"))
            if i != len(self._substitute_for) - 1:
                text.append(("", ", "))

        text.append(("", " to be substituted with "))

        for (i, (resource, amount)) in enumerate(self._substitute_with.items()):
            text.append(("class:count", str(amount)))
            text.append(("", " "))
            text.append(("class:resource", resource.name))
            if amount != 1:
                text.append(("class:resource", "s"))
            if i != len(self._substitute_with) - 1:
                text.append(("", ", "))

        text.append(("", " when purchasing "))
        text.append(("", "tiles"))

        if "pp" in format_spec:
            return text
        if format_spec.isispace or not format_spec:
            return "".join(e[1] for e in text)
        raise ValueError(f"format spec must be either pp or whitespace, was {format_spec!r}")


class BaseWeaponPurchaseEffect(BaseEffect, metaclass=ABCMeta):
    @abstractmethod
    def invoke(self, current_price: Dict[ResourceTypeEnum, int]) -> Dict[ResourceTypeEnum, int]:
        pass


class DecreasePriceOfWeaponEffect(BaseWeaponPurchaseEffect):
    def __init__(
            self,
            decrease_by: Dict[ResourceTypeEnum, int]) -> None:
        if decrease_by is None:
            raise ValueError("Cost to decrease by cannot be none")
        self._decrease_by: Dict[ResourceTypeEnum, int] = decrease_by
        BaseEffect.__init__(self, False)

    def invoke(
            self,
            current_price: Dict[ResourceTypeEnum, int]) \
            -> Dict[ResourceTypeEnum, int]:
        """Returns the new price of the target.

        :param current_price: The current price of the target. This cannot be null.
        :returns: A dictionary of resource type to int containing the new price. This will never be null.
        """
        if current_price is None:
            raise ValueError("Current price cannot be null")

        new_price: Dict[ResourceTypeEnum, int] = dict(current_price)

        for resource in self._decrease_by:
            current_price_for_resource = new_price.get(resource, 0)
            current_price_for_resource -= self._decrease_by[resource]

            new_price[resource] = current_price_for_resource

        return new_price
