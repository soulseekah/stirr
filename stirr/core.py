import json
import zmq
import threading
import backends
import algorithms
from datetime import datetime

class Stirr( object ):
	"""The main `Stirr` class where it all comes into play."""

	debug = None
	configuration = None
	backends = None
	bind = None

	def __init__( self, config='config.json', debug=False, bind='tcp://127.0.0.1:5555' ):
		with open( config, 'rb' ) as c:
			self.configuration = json.load( c )

		self.debug = debug
		self.backends = {}
		self.bind = bind

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
		print( '** Stirring things up on %s...' % self.bind )

		listener = ListenerThread( self )
		listener.daemon = True
		listener.start()

		heartbeat = HeartbeatThread( self ) 
		heartbeat.daemon = True
		heartbeat.start()

		try:
			while True:
				pass
		except KeyboardInterrupt:
			listener.server.close()
			listener.server.context.term()
			print( '** Stopped' )

	def request_handler( self, data ):
		"""Handles an incoming request for data."""

		group = self.backends.get( data.get( 'group', 'default' ), False )
		if not group:
			return { 'error': 'Group %s does not exist.' % data.get( 'group', 'default' ) }

		_type = data.get( 'type', 'Base' )
		backends = filter( lambda b: b.__class__.__name__ == '%sBackend' % _type, group )
		if not len( backends ):
			return { 'error': 'No %sBackends available.' % _type }

		algorithm = data.get( 'algorithm', 'Casual' )
		try:
			algorithm = algorithms.create( algorithm )
		except:
			return { 'error': 'No %sAlgorithm available.' % algorithm }

		backend = algorithm.select( backends, *data.get( 'args', [] ) )

		return backend.configuration

	def heartbeat_state( self, backend, reason ):
		print( '** [%s] %s %s' % ( datetime.now(), backend, reason ) )

class ListenerThread( threading.Thread ):
	"""Main listener."""

	server = None
	container = None

	def __init__( self, container  ):
		threading.Thread.__init__( self )
		self.container = container

	def run( self ):
		context = zmq.Context()
		server = context.socket( zmq.ROUTER )
		server.context = context

		self.server = server
		self.server.bind( self.container.bind )

		poll = zmq.Poller()
		poll.register( server, zmq.POLLIN )

		while True:
			sockets = dict( poll.poll() )
			if server in sockets:
				if sockets[server] == zmq.POLLIN:
					_id = server.recv()
					data = server.recv_json()

					if self.container.debug:
						print( 'Received: %s' % data )

					server.send( _id, zmq.SNDMORE )
					returning = self.container.request_handler( data )
					if self.container.debug:
						print( 'Returning: %s' % returning )
					server.send_json( returning )

class HeartbeatThread( threading.Thread ):
	"""Launches the hearbeat of each backend."""

	container = None

	def __init__( self, container  ):
		threading.Thread.__init__( self )
		self.container = container

	def run( self ):
		for group, _backends in self.container.backends.iteritems():
			for backend in _backends:
				thread = threading.Thread( target=backend.heartbeat, args=[ self.container ] )
				thread.daemon = True
				thread.start()
