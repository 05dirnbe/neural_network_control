#!/usr/bin/python
import argparse, logging, sys
import zmq
import communication
import configuration

def main(args, context):
	# Setup for communication with commander. 
	
	logger = logging.getLogger(__name__)
	settings = configuration.Config()

	controller = communication.connect_socket(context, socket_type = zmq.REQ, connection = settings.connections["commander"])

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

	return


if __name__ == '__main__':

	# Setup for application logging
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(name)s: -- %(levelname)s -- %(message)s', filename="./log/commander.log", filemode="w")
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(name)s: -- %(levelname)s -- %(message)s')
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)

	# Setup for parsing command line arguments
	# see configuration module for options
	parser = argparse.ArgumentParser(prog="commander", description='Generates and sends commands to the controller which interacts with the neural network.')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-q', '--quit', help='Shutdown controller', action='store_true')
	group.add_argument('-p','--pause', help='Put controller in idle state and listen for further commands', action='store_true')
	group.add_argument('-rw','--read_weights', help='Tell controller to read weights', action='store_true')
	group.add_argument('-ww','--write_weights', help='Tell controller to write weights', action='store_true')
	group.add_argument('-rp','--read_parameters', help='Tell controller to read parameters', action='store_true')
	group.add_argument('-wp','--write_parameters', help='Tell controller to write parameters', action='store_true')
	group.add_argument('-rt','--read_topology', help='Tell controller to read network topology', action='store_true')
	group.add_argument('-wt','--write_topology', help='Tell controller to write network topology', action='store_true')
	group.add_argument('-rs','--read_spikes', help='Tell controller to read neuron spikes', action='store_true')
	args = parser.parse_args()

	context = zmq.Context()

	main(args, context)