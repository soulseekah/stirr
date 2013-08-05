from time import time
from multiprocessing import Pool, TimeoutError
from multiprocessing.pool import ThreadPool
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import zmq

def make_request( group='default', type='Base', algorithm='Casual', args=[] ):
	return locals()

def run():
	start = time()
	context = zmq.Context()
	server = context.socket( zmq.DEALER )
	server.connect( ADDRESS )

	server.send_json( make_request( GROUP, TYPE, algorithm=ALGORITHM, args=ARGS ) )
	server.recv_json()

	server.close()
	context.term()

	return time() - start

def main():
	results = []
	start = time()
	pool = ThreadPool( processes=CONCURRENT )
	for _ in xrange( REQUESTS ):
		result = pool.apply_async( run )
		results.append( result )

	timeouts = 0
	times = []

	for result in results:
		try:
			result = result.get( TIMEOUT )
		except TimeoutError:
			timeouts = timeouts + 1
			continue
		times.append( result )

	# pool.close()
	# pool.join()
	end = time()

	print '-' * 32
	print '[%s] %s %s' % ( GROUP, TYPE, ALGORITHM )
	print '%d requests made, with %d at any single time' % ( REQUESTS, CONCURRENT )
	if timeouts: print '** %d request timed out' % ( timeouts )
	print 'total running time: %f seconds' % ( end - start )
	mean = reduce( lambda x, y: x + y, times ) / len( times )
	print 'request time mean: %f, min: %f, max: %f' % ( mean, min( times ), max( times ) )
	print '-' * 32

if __name__ == '__main__':
	parser = ArgumentParser(
		description='A benchmark tool for stirr.',
		formatter_class=ArgumentDefaultsHelpFormatter
	)

	parser.add_argument(
		'-p', nargs='?', default=16,
		help='the maximum number of concurrent of requests to enable'
	)

	parser.add_argument(
		'-n', nargs='?', default=1000,
		help='the total number of requests to perform'
	)

	parser.add_argument(
		'--bind', nargs='?', default='tcp://127.0.0.1:5555',
		metavar='ADDRESS',
		help='the address string in the form of protocol://interface:port'
	)

	parser.add_argument(
		'-t', nargs='?', default=1,
		metavar='TIMEOUT',
		help='the timeout for a request, in seconds'
	)

	parser.add_argument(
		'--backend', default=[ 'fortune', 'Base', 'Casual' ],
		metavar='[group] [type] [algorithm] [args]',
		help='the backend to be used'
	)

	args = vars( parser.parse_args() )

	defaults = [ 'fortune', 'Base', 'Casual', '' ]
	backend = args.get( 'backend' )
	backend = backend + defaults[len( backend ):]
	GROUP, TYPE, ALGORITHM, ARGS = backend
	ARGS = ARGS.split( ' ' ) 
	ADDRESS = args.get( 'bind' )
	CONCURRENT = int( args.get( 'p' ) )
	REQUESTS = int( args.get( 'n' ) )
	TIMEOUT = int( args.get( 't' ) )
	
	main()
