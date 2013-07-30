def create( type='Base', group='default', weight=1.0, configuration=None ):
	"""Creates a Backend of a certain type."""

	if not globals().get( type.lower() , False ):
		__import__( 'stirr.backends.%s' % type.lower() )

	Backend = getattr( globals().get( type.lower() ), '%sBackend' % type )

	return Backend( group, weight, configuration )
