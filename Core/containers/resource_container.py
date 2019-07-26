from typing import Dict
from core.enums.caverna_enums import ResourceTypeEnum

class ResourceContainer(object):
    _resources: Dict[ResourceTypeEnum, int] = {}
    
    def has_resources(self) -> bool:
        if self._resources is None:
            return False
        
        any = False
        for resource in self._resources:
            any |= self._resources[resource] != 0
        
        return any
    
    def get_resources(self) -> Dict[ResourceTypeEnum, int]:
        return dict(self._resources)
        
    def give_resource(self, type: ResourceTypeEnum, amount: int) -> bool:
        if amount < 0:
            #raise ValueError("amount")
            return False
    
        currentAmount = self._resources.setdefault(type, 0)
        self._resources[type] = currentAmount + amount
        return True
        
    def give_resources(self, resources: Dict[ResourceTypeEnum, int]) -> bool:
        if resources is None:
            #raise ValueError("resources")
            return False
        
        any = True
        for resource in resources:
            any &= self.give_resource(resource, resources[resource])
        return any
            
    def take_resource(self, type: ResourceTypeEnum, amount: int) -> bool:
        if amount < 0:
            #raise ValueError("amount")
            return False
            
        currentAmount = self._resources.setdefault(type, 0)
        if currentAmount < amount:
            return False
        
        self._resources[type] = currentAmount - amount
        return True
        
    def take_resources(self, resources: Dict[ResourceTypeEnum, int]) -> bool:
        if resources is None:
            #raise ValueError("resources")
            return False
        
        any = True
        for resource in resources:
            any &= self.give_resource(resource, resources[resource])
        return any
        
    def clear_resources(self) -> bool:
        for resource in self._resources:
            self._resources[resource] = 0
        return True