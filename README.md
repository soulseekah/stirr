`stirr` is a [zmq](http://zeromq.org/)-supported backend manager that can be queried for backend configurations.

##Installation

`python setup.py install` should do the trick, so should `pip install .`, in theory.

##Usage

Simple: `stirr -h`

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

##Built-ins

###Balancing algorithms

- `Casual` - a seemingly random selection algorithm that doesn't take weights into account.
- `Weighted` - weight-based randomization, similar to `Casual` but biased.

##Backend types

- `Base` - a backend that is always up, never performs any heartbeat checks.
