from algorithms.base import BaseAlgorithm
from random import choice

class WeightedAlgorithm( BaseAlgorithm ):
	"""A random selection, weighted."""

	def select( self, backends, *args ):
		_backends = []

		for n, backend in enumerate( backends ):
			_backends += [n] * int( backend.weight * 1000 )

		return backends[choice( _backends )]
