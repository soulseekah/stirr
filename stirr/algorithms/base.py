class BaseAlgorithm( object ):
	"""The base algorithm object that selects a backend."""

	def select( self, backends, *args ):
		raise NotImplementedError
