#!/usr/bin/python
import argparse, logging, sys
import zmq
from communication import *

def main(args, context):
	# Setup for communication with commander. 
	
	logger = logging.getLogger(__name__)

	controller = connect_socket(context, socket_type = zmq.REQ, connection = connections["commander"])

	command = None
	for arg in vars(args):
		if getattr(args, arg):
			command = arg

	if command:

		try:
			logger.info("Command: %s", command)
			controller.send(command)
			message = controller.recv()

			logger.debug("Controller executed command: %s", message)
			assert(command == message)

		except Exception as e:
			logger.exception("Command failed.")
			logger.info("Shutting down commander.")
			sys.exit()

	else:
		logger.info("No command selected. Use -h | --help to see options.")



if __name__ == '__main__':

	# Setup for application logging
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(name)s: -- %(levelname)s -- %(message)s', filename="./log/commander.log", filemode="w")
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(name)s: -- %(levelname)s -- %(message)s')
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)

	# Setup for parsing command line arguments
	parser = argparse.ArgumentParser(prog="commander", description='Generates and sends commands to the controller which interacts with the neural network.')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-q', '--quit', help='Shutdown controller', action='store_true')
	group.add_argument('-p','--pause', help='Put controller in idle state', action='store_true')
	group.add_argument('-rw','--read_weights', help='Tell controller to read weights', action='store_true')
	group.add_argument('-ww','--write_weights', help='Tell controller to write weights', action='store_true')
	group.add_argument('-rp','--read_parameters', help='Tell controller to read parameters', action='store_true')
	group.add_argument('-wp','--write_parameters', help='Tell controller to write parameters', action='store_true')
	args = parser.parse_args()

	context = zmq.Context()

	main(args, context)