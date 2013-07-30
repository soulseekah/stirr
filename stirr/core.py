import json
import backends

class Stirr( object ):
	"""The main `Stirr` class where it all comes into play."""

	debug = None
	configuration = None
	backends = None

	def __init__( self, config='config.json', debug=False ):
		with open( config, 'rb' ) as c:
			self.configuration = json.load( c )

		self.debug = debug
		self.backends = {}

		for backend in self.configuration.get( 'backends', [] ):
			if type( backend ) is dict:
				backend = backends.create( **backend )
				if self.backends.get( backend.group, False ):
					self.backends.get( backend.group ).append( backend )
					self.backends.get( backend.group ).sort( key=lambda b: b.weight, reverse=True )
				else:
					self.backends.update( { backend.group: [ backend ] } )


		if self.debug:
			print( 'Configuration %s:' % config )
			
			for group, _backends in self.backends.iteritems():
				print( '\tGroup: %s' % group )
				for backend in _backends:
					print( '\t\t%s' % backend )

	def run( self ):
		print( '** Stirring things up...' )
