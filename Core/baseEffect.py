class BaseEffect(object):

	def Invoke(
		self,
		player ) -> bool:
		raise NotImplementedError("abstract base effect class")