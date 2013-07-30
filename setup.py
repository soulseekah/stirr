from setuptools import setup, find_packages

setup(
	name = 'stirr',
	version = '0.1',
	description = 'A load-balancing backend configuration manager.',
	keywords = ( 'load-balance', 'system', 'web' ),
	author = 'Gennady Kovshenin',
	author_email = 'gennady@kovshenin.com',
	url = 'https://github.com/soulseekah/stirr',

	packages = find_packages(),
	entry_points = {
		'console_scripts': [ 'stirr = stirr.stirr:main' ]
	},
	
	install_requires = [ 'pyzmq' ],
)
