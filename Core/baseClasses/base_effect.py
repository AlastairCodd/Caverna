from core.enums.cavernaEnums import TriggerStateEnum

class BaseEffect(object):
	def __init__(self, triggerState = TriggerStateEnum.UserChoice):
		self._triggerState = triggerState

	def invoke(
		self,
		player ) -> bool:
		raise NotImplementedError("abstract base effect class")
