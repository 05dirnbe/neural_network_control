import logging

logger = logging.getLogger(__name__)
socket_name = { 4 : "zmq.REP", 3: "zmq.REQ" }
connections = {	"commander"	:	"tcp://localhost:5555",
				"controller"	:	"tcp://*:5555",
			  }

def bind_socket(context, socket_type, connection):

    logger.info("Binding Type %s socket to: %s", socket_name[socket_type], connection)
    sock = context.socket(socket_type)
    sock.bind(connection)

    return sock

def connect_socket(context, socket_type, connection):

    logger.info("Connecting Type %s socket to: %s", socket_name[socket_type], connection)
    sock = context.socket(socket_type)
    sock.connect(connection)

    return sock