from stirr.algorithms.base import BaseAlgorithm
from random import choice

class CasualAlgorithm( BaseAlgorithm ):
	"""A random selection, non-weighted."""

	def select( self, backends, *args ):
		return choice( backends )
