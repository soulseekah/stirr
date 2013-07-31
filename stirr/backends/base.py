class BaseBackend( object ):
	"""A base backend class."""

	group = None
	weight = None
	configuration = None

	def __init__( self, group="default", weight=1.0, configuration=None, args=[] ):
		self.group = group
		self.weight = weight
		self.configuration = configuration

	def heartbeat( self ):
		"""Are we alive?"""
		return True

	def __str__( self ):
		return '%s [%.02f], %s' % \
			( self.__class__.__name__, self.weight, self.configuration )

	def __unicode__( self ):
		return self.__str__()
