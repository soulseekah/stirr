from stirr.backends.base import BaseBackend
import subprocess
import time

class MySQLBackend( BaseBackend ):
	"""A MySQL backend."""

	credentials = None
	health = 100 # Initial assumed health

	def __init__( self, group="default", weight=1.0, heartbeat=30, configuration=None, args=[] ):
		BaseBackend.__init__( self, group, weight, heartbeat, configuration, args )

		args += [ None, None, None, None, None ] # At least these
		args.reverse()
		self.credentials = {
			'user': args.pop() or 'root',
			'pass': args.pop() or '',
			'host': args.pop() or 'localhost',
			'port': args.pop() or 3306,
			'limit': args.pop() or 16,
		}

	def heartbeat( self, container ):
		"""Checks and records the status of this particular MySQL server."""

		while True:
			process = subprocess.Popen( [
				'mysqladmin',
				'--user=%s' % self.credentials.get( 'user' ),
				'--password=%s' % self.credentials.get( 'pass' ),
				'--host=%s' % self.credentials.get( 'host' ),
				'--port=%s' % self.credentials.get( 'port' ),
				'--connect_timeout=10',
				'extended-status'
			], stdout=subprocess.PIPE, stderr=subprocess.STDOUT )

			process.wait()

			if process.returncode != 0:
				if self.health > 0:
					self.health = 0
					reason = 'is down: %s' % process.stdout.readline().strip()
					container.heartbeat_state( self, reason )
			else:
				for line in process.stdout:
					if 'threads_connected' in line.lower():
						threads = int( line.split( '|' )[2] )
						break

				assert type( threads ) is int

				health = ( 1 - ( float( threads ) / float( self.credentials.get( 'limit' ) ) ) )* 100
				health = int( health * self.weight )

				if self.health < 1 and health > 0:
					container.heartbeat_state( self, 'is up again...' )

				self.health = health

			time.sleep( self.heartbeat_interval )
