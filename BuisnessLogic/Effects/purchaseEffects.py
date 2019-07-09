from typing import Dict

class BasePurchaseEffect(BaseEffect):
	'''Abstract class for purchase effects'''
	
	def invoke(self):
		raise NotImplementedError()
	
class DecreasePrice(BasePurchaseEffect):
	def __init__(self, decreaseBy, subject):
		self._subject = subject
		self._decreaseBy = decreaseBy
	
	def invoke(self, target) -> Dict[ResourceTypeEnum, int]:
		'''Decrease the current price of target by self._decreaseBy
			to a minimum cost of 0
			
			Target: either a tileTypeEnum
		price = dict(target.get_price())
		for key in self._decreaseBy:
			currentPriceForKey = price.get(key, 0)
			targetPriceForKey = currentPriceForKey - self._decreaseBy[key]
			targetPriceForKey = max(0, targetPriceForKey)
			price[key] = targetPriceForKey
		return price