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

command_to_int = {"quit":0, "pause":1, "read_weights":2}

args = parser.parse_args()
command = None

for arg in vars(args):
	if getattr(args, arg):
		command = arg

if command:

	command = command_to_int[command]

	context = zmq.Context()
	socket = context.socket(zmq.PAIR)
	socket.connect(host)

	logging.info("Sending command: %d to port %s at host %s.", command, port, host)

	socket.send(command)
	message = socket.recv()
	logging.info("Received echo from server:%d", message)

else:
	logging.info("No command selected. Use -h | --help to see options.")