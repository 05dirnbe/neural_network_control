#!/usr/bin/python
import argparse, logging, sys, time
import zmq
from communication import *

def main(args, context):
	
	logger = logging.getLogger(__name__)

	output_data = connect_socket(context, socket_type = zmq.SUB, connection = connections["output_data"])
	output_data.setsockopt(zmq.SUBSCRIBE,topics["parameters"])

	logger.info("Listening for data stream.")

	try:

		while True:
			
			message = output_data.recv()
			logger.info("Recieved: %s", message)
			time.sleep(args.s)
		
	except Exception as e:
		logger.exception("Listening failed.")
		logger.info("Shutting down monitor.")
		sys.exit()

	except KeyboardInterrupt as e:
		logger.debug("User interrupt.")
		logger.info("Shutting down monitor.")
		sys.exit()

	return

if __name__ == '__main__':

	# Setup for application logging
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(name)s: -- %(levelname)s -- %(message)s', filename="./log/parameter_monitor.log", filemode="w")
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(name)s: -- %(levelname)s -- %(message)s')
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)

	# Setup for parsing command line arguments
	parser = argparse.ArgumentParser(prog="parameter_monitor", description='Monitors the output of the controller regarding parameters.')
	parser.add_argument('-s', help='Number of seconds to sleep in between two revieves.', type=float, default=0)
	args = parser.parse_args()

	context = zmq.Context()

	main(args, context)