from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from core import Stirr

def main():
	"""The main `stirr` CLI entry point."""

	parser = ArgumentParser(
		description='A load-balancing backend configuration manager.',
		formatter_class=ArgumentDefaultsHelpFormatter
	)

	parser.add_argument(
		'-c', '--config',
		nargs='?', default='config.json',
		help='the configuration file to load',
	)
	parser.add_argument(
		'--debug', '-d', action='store_true',
		help='output debug information',
	)
	parser.add_argument(
		'--bind', nargs='?', default='tcp://127.0.0.1:5555',
		metavar='ADDRESS',
		help='the address string in the form of protocol://interface:port'
	)

	args = parser.parse_args()

	if args.debug:
		print( 'Arguments:' )
		for k, v in vars( args ).iteritems():
			print( '\t%s: %s' % ( k, v ) )

	stirr = Stirr( **vars( args ) )
	stirr.run()
