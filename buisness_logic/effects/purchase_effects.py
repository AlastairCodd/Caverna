import math
from abc import ABCMeta, abstractmethod
from typing import Dict, Union, Type, List
from core.services.base_player_service import BasePlayerService
from common.entities.weapon import Weapon
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class BasePurchaseEffect(BaseEffect, metaclass=ABCMeta):
    """Abstract class for purchase effects"""

    @abstractmethod
    def invoke(
            self,
            player: BasePlayerService,
            target: Union[BaseTile, Weapon],
            current_price: Dict[ResourceTypeEnum, int]) \
            -> Dict[ResourceTypeEnum, int]:
        """Returns the new price of the target.

        :param player: The player who is attempting to purchase the item.
        :param target: The object whose price may be decreased. This cannot be null.
        :param current_price: The current price of the target. This cannot be null.
        :returns: A dictionary of resource type to int containing the new price. This will never be null.
        """
        raise NotImplementedError()


class DecreasePrice(BasePurchaseEffect):
    def __init__(
            self,
            subject: Union[BaseTile, Weapon, Type],
            decrease_by: Dict[ResourceTypeEnum, int]):
        """Decreases the price required to purchase something (either a tile, including pastures and stables or weapons)

        :param subject: The object which is effected by this discount. This cannot be null.
        :param decrease_by: The amount to decrease the cost by (down to a minimum of 0). This cannot be null.
        """
        if subject is None:
            raise ValueError("Subject cannot be none")
        if decrease_by is None:
            raise ValueError("Amount to decrease by cannot be null.")
        self._subject_type: Type = subject if isinstance(subject, type) else type(subject)
        self._decreaseBy: Dict[ResourceTypeEnum] = decrease_by
        BaseEffect.__init__(self)

    def invoke(
            self,
            player: BasePlayerService,
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

        if not isinstance(target, self._subject_type):
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


class AllowSubstitutionForPurchase(BaseEffect):
    def __init__(
            self,
            subject: Union[BaseTile, Weapon, Type],
            substitute_for: Dict[ResourceTypeEnum, int],
            substitute_with: Dict[ResourceTypeEnum, int],
            allow_multiple: bool = False):
        """Generates alternative costs by substituting x for y

        :param subject: The object which is effected by this discount. This cannot be null.
        :param substitute_for: The portion of the price to be removed. This cannot be null.
        :param substitute_with: The portion of the price to be added. This cannot be null.
        :param allow_multiple: Allow the substitution to be performed multiple times.
        """
        if subject is None:
            raise ValueError("Subject cannot be null")
        if substitute_for is None:
            raise ValueError("Substitute for cannot be null")
        if substitute_with is None:
            raise ValueError("Substitute with cannot be null")
        self._subject_type: Type = subject if isinstance(subject, type) else type(subject)
        self._substitute_for: Dict[ResourceTypeEnum, int] = substitute_for
        self._substitute_with: Dict[ResourceTypeEnum, int] = substitute_with
        self._allow_multiple: bool = allow_multiple

        BaseEffect.__init__(self)

    def invoke(
            self,
            player: BasePlayerService,
            # TODO: Change this
            target: Union[BaseTile, Weapon],
            current_price: Dict[ResourceTypeEnum, int]) -> Dict[ResourceTypeEnum, int]:
        """Returns the new price of the target.

        :param player: The player who is attempting to purchase the item. This cannot be null.
        :param target: The object whose price may be decreased. This cannot be null.
        :param current_price: The current price of the target. This cannot be null.
        :returns: A dictionary of resource type to int containing the new price. This will never be null.
        """
        if player is None:
            raise ValueError("Player cannot be null")
        if target is None:
            raise ValueError("Target cannot be null")
        if current_price is None:
            raise ValueError("Current price cannot be null")

        if not isinstance(target, type(self._subject_type)):
            return current_price

        number_of_times_substitute_for_is_in_current_price: int = self.times_contained(
            current_price,
            self._substitute_for)

        possible_prices: List[Dict[ResourceTypeEnum, int]] = []

        if self._allow_multiple and number_of_times_substitute_for_is_in_current_price > 1:
            number_of_times_substitute_for_is_in_current_price = 1

        for i in range(number_of_times_substitute_for_is_in_current_price + 1):
            price: Dict[ResourceTypeEnum, int] = dict(current_price)

            if i == 0:
                possible_prices.append(price)
                continue

            for resource_to_remove, amount_to_remove in self._substitute_for.items():
                price[resource_to_remove] -= amount_to_remove * i
            for resource_to_add, amount_to_add in self._substitute_with.items():
                price[resource_to_add] = price.get(resource_to_add, 0) + amount_to_add * i
            possible_prices.append(price)

        if len(possible_prices) > 1:
            new_price = player.get_player_choice_discount(possible_prices, target)
        else:
            new_price = current_price

        return new_price

    def times_contained(
            self,
            query_set: Dict[ResourceTypeEnum, int],
            subset: Dict[ResourceTypeEnum, int]) \
            -> int:
        """Gets the number of occurrences of the dictionary "set" in the dictionary "query_set".

        :param query_set: The dictionary to be queried. This cannot be null.
        :param subset: The dictionary which will be searched for. This cannot be null.
        :return: The number of occurrences of the dictionary. Greater than 0.
        """
        number_of_occurrences_of_subset_in_set: int = -1

        for resource, quantity in subset.items():
            number_of_times: int = math.floor(query_set.get(resource, 0) / quantity)
            if number_of_times < number_of_occurrences_of_subset_in_set or \
                    number_of_occurrences_of_subset_in_set == -1:
                number_of_occurrences_of_subset_in_set = number_of_times
            if number_of_times == 0:
                break

        return number_of_occurrences_of_subset_in_set
