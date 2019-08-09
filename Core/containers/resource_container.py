from typing import Dict
from core.enums.caverna_enums import ResourceTypeEnum


class ResourceContainer(object):
    def __init__(self):
        self._resources: Dict[ResourceTypeEnum, int] = {}

    @property
    def has_resources(self) -> bool:
        if self._resources is None:
            return False

        result = False
        for resource in self._resources:
            result |= self._resources[resource] != 0

        return result

    @property
    def resources(self) -> Dict[ResourceTypeEnum, int]:
        result = {
            ResourceTypeEnum.stone: self._resources.get(ResourceTypeEnum.stone, 0),
            ResourceTypeEnum.wood: self._resources.get(ResourceTypeEnum.wood, 0),
            ResourceTypeEnum.ore: self._resources.get(ResourceTypeEnum.ore, 0),
            ResourceTypeEnum.ruby: self._resources.get(ResourceTypeEnum.ruby, 0),
            ResourceTypeEnum.coin: self._resources.get(ResourceTypeEnum.coin, 0),
            ResourceTypeEnum.food: self._resources.get(ResourceTypeEnum.food, 0),
            ResourceTypeEnum.grain: self._resources.get(ResourceTypeEnum.grain, 0),
            ResourceTypeEnum.veg: self._resources.get(ResourceTypeEnum.veg, 0),
            ResourceTypeEnum.sheep: self._resources.get(ResourceTypeEnum.sheep, 0),
            ResourceTypeEnum.donkey: self._resources.get(ResourceTypeEnum.donkey, 0),
            ResourceTypeEnum.cow: self._resources.get(ResourceTypeEnum.cow, 0),
            ResourceTypeEnum.boar: self._resources.get(ResourceTypeEnum.boar, 0),
            ResourceTypeEnum.dog: self._resources.get(ResourceTypeEnum.dog, 0),
        }
        return result

    def get_resources_of_type(self, resource_type: ResourceTypeEnum) -> int:
        result = self._resources.get(resource_type, 0)
        return result

    def give_resource(self, resource_type: ResourceTypeEnum, amount: int) -> bool:
        if amount < 0:
            return False

        current_amount = self._resources.setdefault(type, 0)
        self._resources[resource_type] = current_amount + amount
        return True

    def give_resources(self, resources: Dict[ResourceTypeEnum, int]) -> bool:
        if resources is None:
            return False

        success = True
        for resource in resources:
            success &= self.give_resource(resource, resources[resource])
        return success

    def take_resource(self, resource_type: ResourceTypeEnum, amount: int) -> bool:
        if amount < 0:
            return False

        current_amount = self._resources.setdefault(resource_type, 0)
        if current_amount < amount:
            return False

        self._resources[resource_type] = current_amount - amount
        return True

    def take_resources(self, resources: Dict[ResourceTypeEnum, int]) -> bool:
        if resources is None:
            return False

        success = True
        for resource in resources:
            success &= self.give_resource(resource, resources[resource])
        return success

    def clear_resources(self) -> bool:
        for resource in self._resources:
            self._resources[resource] = 0
        return True
