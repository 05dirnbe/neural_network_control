#!/usr/bin/python
import argparse, logging, sys, time
import zmq
import communication
import configuration
import serialization

def main(args, context):
	
	logger = logging.getLogger(__name__)
	settings = configuration.Config()
	serializer = serialization.Serializer()

	output_data = communication.connect_socket(context, socket_type = zmq.SUB, connection = settings.connections["output_data"])
	output_data.setsockopt(zmq.SUBSCRIBE,settings.topics["topology"])

	logger.info("Listening for data stream.")

	try:

		while True:
			
			message_buffer = output_data.recv()
			message = serializer.read_buffer(message_buffer, topic = "topology")
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
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(name)s: -- %(levelname)s -- %(message)s', filename="./log/weight_monitor.log", filemode="w")
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(name)s: -- %(levelname)s -- %(message)s')
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)

	# Setup for parsing command line arguments
	parser = argparse.ArgumentParser(prog="topology_monitor", description='Monitors the output of the controller regarding network topology.')
	parser.add_argument('-s', help='Number of seconds to sleep in between two recieves.', type=float, default=0)
	args = parser.parse_args()

	context = zmq.Context()

	main(args, context)