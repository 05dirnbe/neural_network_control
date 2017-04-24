import logging

logger = logging.getLogger(__name__)

socket_name = { 6: "zmq.ROUTER", 5: "zmq.DEALER", 4 : "zmq.REP", 3: "zmq.REQ", 2: "zmq.SUB", 1: "zmq.PUB" }

connections = {	"commander"	:	"tcp://localhost:5555",
				"controller"	:	"tcp://*:5555",
				"input_data"	:	"tcp://localhost:5556",
				"camera"	:	"tcp://*:5556",
				"output_data"	:	"tcp://localhost:5557",
				"monitor"	:	"tcp://*:5557",
			  }

topics = {"weights" : "weights", "parameters" : "parameters", "spikes" : "spikes", "topology" : "topology" }


def bind_socket(context, socket_type, connection):

    logger.info("Binding %s socket to: %s", socket_name[socket_type], connection)
    sock = context.socket(socket_type)
    sock.bind(connection)

    return sock

def connect_socket(context, socket_type, connection):

    logger.info("Connecting %s socket to: %s", socket_name[socket_type], connection)
    sock = context.socket(socket_type)
    sock.connect(connection)

    return sock