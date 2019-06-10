from typing import Dict
from Core.cavernaEnums import ResourceTypeEnum

class ResourceContainer(object):
	def __init__(self):
		self._resources: Dict[ResourceTypeEnum, int] = {}

	def HasResources(self) -> bool:
		if self._resources is None:
			return False
		
		any = False
		for resource in self._resources:
			any |= self._resources[resource] != 0
		
		return any
	
	def GetResources(self) -> Dict[ResourceTypeEnum, int]:
		return self._resources
		
	def GiveResource(self, type: ResourceTypeEnum, amount: int) -> bool:
		if amount < 0:
			#raise ValueError("amount")
			return False
	
		currentAmount = self._resources.setdefault(type, 0)
		self._resources[type] = currentAmount + amount
		return True
		
	def GiveResources(self, resources: Dict[ResourceTypeEnum, int]) -> bool:
		if resources is None:
			#raise ValueError("resources")
			return False
		
		any = True
		for resource in resources:
			any &= self.GiveResource(resource, resources[resource])
		return any
			
	def TakeResource(self, type: ResourceTypeEnum, amount: int) -> bool:
		if amount < 0:
			#raise ValueError("amount")
			return False
			
		currentAmount = self._resources.setdefault(type, 0)
		if currentAmount < amount:
			return False
		
		self._resources[type] = currentAmount - amount
		return True
		
	def TakeResources(self, resources: Dict[ResourceTypeEnum, int]) -> bool:
		if resources is None:
			#raise ValueError("resources")
			return False
		
		any = True
		for resource in resources:
			any &= self.GiveResource(resource, resources[resource])
		return any
		
	def ClearResources(self) -> bool:
		for resource in self._resources:
			self._resources[resource] = 0
		return True
		
class ActiveResourceContainer(ResourceContainer):
	
	def RefillAction(self):
		raise NotImplementedError("abstract base class")