`stirr` is a [zmq](http://zeromq.org/)-supported backend manager that can be queried for backend configurations. `stirr` will try to load-balance backend/service access by sending different configuration data upon request. Configuration data is arbitrary and defined using a JSON syntax.

##Installation

`python setup.py install` should do the trick, so should `pip install .`, in theory.

##Usage

```
usage: stirr [-h] [-c [CONFIG]] [--debug] [--bind [ADDRESS]]

A load-balancing backend configuration manager.

optional arguments:
  -h, --help            show this help message and exit
  -c [CONFIG], --config [CONFIG]
                        the configuration file to load (default: config.json)
  --debug, -d           output debug information (default: False)
  --bind [ADDRESS]      the address string in the form of
                        protocol://interface:port (default:
                        tcp://127.0.0.1:5555)
```

###Configuration

Configurations are defined using JSON syntax as follows:

```json
{
	"backends": [
		"all strings are mere comments" (optional),

		{
			"group": "default" (optional),
			"type": "Base" (required, can be array with arguments [ "MySQL", "root", "letmein" ] for some backends)
			"weight": 1.0 (optional),
			"heartbeat": 15 (optional),
			"configuration": <arbitrary structure> (required)
		}
	]
}
```

###Client API

All communication is done via zmq using JSON serialization. Since there is no encryption `stirr` should probably only be used on the localhost. No sensitive data should be passed over the wire. See the `examples` directory for a sample client.

A typical request payload would look like:

```json
{
	"group": "default",
	"type": "Base",
	"algorithm": "Casual",
	"args": [],
}
```

The response is the `configuration` dump of the chosen backend. An `error` can be sent inside the JSON response if someting is wrong.

##Built-ins

###Balancing algorithms

- `Casual` - a seemingly random selection algorithm that doesn't take weights into account.
- `Weighted` - weight-based randomization, similar to `Casual` but biased.

###Backend types

- `Base` - a backend that is always up, never performs any heartbeat checks.
