import json
import zmq
import threading
import backends

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

class ListenerThread( threading.Thread ):
	"""Main listener."""

	server = None
	containter = None

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
					server.send_json( data )

class HeartbeatThread( threading.Thread ):
	"""Heartbeat, checks the validity of each backend."""

	containter = None

	def __init__( self, container  ):
		threading.Thread.__init__( self )
		self.container = container

	def run( self ):
		while True:
			pass

