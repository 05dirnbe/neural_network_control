#!/usr/bin/python
import argparse, logging, sys, time, os
import zmq
import communication
import configuration
import serialization

class Data_logger(object):

	def __init__(self, topic, path, sleep = 0, connection = "output_data" , settings = configuration.Config(), serializer = serialization.Serializer()):

		self.context = zmq.Context()
		self.settings = settings
		self.serializer = serializer
		self.sleep = sleep

		self.data = communication.connect_socket(self.context, socket_type = zmq.SUB, connection = self.settings.connections[connection])
		self.data.setsockopt(zmq.SUBSCRIBE, self.settings.topics[topic])

		self.logger = logging.getLogger(topic + "_logger")

		self.topic = topic
		self.folder = os.path.join(path, topic)
		self.log_file = os.path.join(self.folder, topic+"_store"+".txt")

	def prepare_save(self, folder):

		if not os.path.exists(folder):
			self.logger.info("Creating directory: %s", folder)
			os.makedirs(folder)

	def serve_forever(self):

		try:

			self.prepare_save(self.folder)

			with open(self.log_file, "w") as store:

				self.logger.info("Starting to log to file: %s", self.log_file)

				while True:
					
					topic, message_buffer = self.data.recv().split()
					message = self.serializer.read_buffer(message_buffer, topic = topic)
					store.write(message_buffer+"\n")
					self.logger.debug("Recieved: %s", message)

					time.sleep(self.sleep)
								
		except Exception as e:
			self.logger.exception("Listening failed.")
			self.logger.info("Shutting down monitor.")
			sys.exit()

		except KeyboardInterrupt as e:
			self.logger.info("User interrupt.")
			self.logger.info("Shutting down monitor.")
			sys.exit()

def main(args):
	
	data_logger = Data_logger(topic = args.topic, path = args.path, sleep = args.s)
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
	data_logger = Data_logger(topic = args.topic, path = args.path, sleep = args.s)
	data_logger.serve_forever()

	main(args)