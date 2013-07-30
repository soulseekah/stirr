def create( type='Casual' ):
	"""Creates an Algorithm of a certain type."""

	if not globals().get( type.lower() , False ):
		__import__( 'algorithms.%s' % type.lower() )

	Algorithm = getattr( globals().get( type.lower() ), '%sAlgorithm' % type )

	return Algorithm()
