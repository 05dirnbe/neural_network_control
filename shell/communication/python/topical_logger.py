#!/usr/bin/python
import argparse, logging, sys, time, os
import zmq
import communication
import configuration
import serialization
import monitoring

def main(args):
	
	data_logger = monitoring.FileLogger(topic = args.topic, path = args.path, sleep = args.s)
	data_logger.serve_forever()

if __name__ == '__main__':

	# Setup for parsing command line arguments
	parser = argparse.ArgumentParser(description='Logs the data output of the controller for a specified topic.')
	parser.add_argument('-s', metavar="seconds", help='Number of seconds to sleep in between two recieves.', type=float, default=0)
	parser.add_argument('-t','--topic', metavar="topic", default = "spikes", help='Specify the topic for data logging', )
	parser.add_argument('-p','--path', metavar="path", default = "log/data", help='Folder to store data logs', )
	parser.add_argument('-v','--verbose', action='store_true', default = False, help='tell controller to write weights', )
	args = parser.parse_args()

	if args.verbose:
		log_level = logging.INFO
	else:
		log_level = logging.DEBUG

	# Setup for application logging
	logging.basicConfig(level=logging.INFO, format='%(name)s: -- %(levelname)s -- %(message)s')
	
	main(args)