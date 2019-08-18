from core.baseClasses.base_action import BaseAction


class GetABabyDwarfAction(BaseAction):
	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		if player is None:
			raise ValueException("player")
		raise NotImplementedException
		