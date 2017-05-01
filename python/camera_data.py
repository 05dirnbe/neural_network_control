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

	input_data = communication.connect_socket(context, socket_type = zmq.PUB, connection = settings.connections["input_data"])
	
	logger.info("Starting data stream. Sending %d elements.", args.n)

	try:

		for i in xrange(args.n):
			
			logger.debug("Sending: %s", str(i))

			message = i
			message_buffer = serializer.write_buffer(message, topic = "camera")
			input_data.send(message_buffer)
			
			time.sleep(args.s)
		
		logger.info("Data transfer complete.")

	except Exception as e:
			logger.exception("Failed sending camera data.")
			logger.info("Shutting down camera data stream.")
			sys.exit()

	return

if __name__ == '__main__':

	# Setup for application logging
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(name)s: -- %(levelname)s -- %(message)s', filename="./log/camera_data.log", filemode="w")
	console = logging.StreamHandler()
	console.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(name)s: -- %(levelname)s -- %(message)s')
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)

	# Setup for parsing command line arguments
	parser = argparse.ArgumentParser(prog="camera_data", description='Simulates the behaviour of the camera generating relevant data.')
	parser.add_argument('-n', help='Number of data events to be send.', type=int, default=10)
	parser.add_argument('-s', help='Number of seconds to sleep in between two sends.', type=float, default=1)
	args = parser.parse_args()

	context = zmq.Context()

	main(args, context)