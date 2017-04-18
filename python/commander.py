#!/usr/bin/python
import argparse, logging
import zmq

port = "5555"
host = "tcp://localhost:%s" % port

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(name)s: -- %(levelname)s -- %(message)s')

parser = argparse.ArgumentParser(prog="commander", description='Generates and sends commands to the controller which interacts with the neural network.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quit', help='Shutdown controller', action='store_true')
group.add_argument('-p','--pause', help='Put controller in idle state', action='store_true')
group.add_argument('-rw','--read_weights', help='Tell controller to read weights', action='store_true')
group.add_argument('-ww','--write_weights', help='Tell controller to write weights', action='store_true')
group.add_argument('-rp','--read_parameters', help='Tell controller to read parameters', action='store_true')
group.add_argument('-wp','--write_parameters', help='Tell controller to write parameters', action='store_true')

args = parser.parse_args()
command = None

for arg in vars(args):
	if getattr(args, arg):
		command = arg

if command:

	context = zmq.Context()
	socket = context.socket(zmq.PAIR)
	socket.connect(host)

	logging.info("Sending command: %s to port %s at host %s.", command, port, host)

	socket.send(command)
	message = socket.recv()
	logging.info("Received echo from server:%s", message)

else:
	logging.info("No command selected. Use -h | --help to see options.")