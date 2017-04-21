#!/usr/bin/python
import argparse, logging, sys, time
import zmq
from communication import *

def main(args, context):
	
	logger = logging.getLogger(__name__)

	input_data = connect_socket(context, socket_type = zmq.PUB, connection = connections["camera_data"])

	logger.info("Starting data stream. Sending %d elements.", args.n)

	try:

		for i in xrange(args.n):
			
			message = str(i)

			logger.info("Sending: %s", message)
			input_data.send("Camera data packet %s" % message)
			time.sleep(args.s)
		
		logger.info("Data transfer complete.")

	except Exception as e:
			logger.exception("Failed sending camera data.")
			logger.info("Shutting down camera data stream.")
			sys.exit()

if __name__ == '__main__':

	# Setup for application logging
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(name)s: -- %(levelname)s -- %(message)s', filename="./log/camera_data.log", filemode="w")
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(name)s: -- %(levelname)s -- %(message)s')
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)

	# Setup for parsing command line arguments
	parser = argparse.ArgumentParser(prog="camera_data", description='Simulates the behaviour of the camera generating relevant data.')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-n', help='Number of data events to be send.', type=int, default=10)
	group.add_argument('-s', help='Number of seconds to sleep in between two sends.', type=int, default=1)
	args = parser.parse_args()

	context = zmq.Context()

	main(args, context)