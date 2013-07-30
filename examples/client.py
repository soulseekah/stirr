import zmq

def make_request( group='default', type='Base', algorithm='random' ):
	return locals()

context = zmq.Context()
server = context.socket( zmq.DEALER )
server.connect( 'tcp://127.0.0.1:5555' )

server.send_json( make_request( 'fortune' ) )

print server.recv_json()

server.close()
context.term()
