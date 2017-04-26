#!/usr/bin/python
import argparse, logging, sys
import zmq
import communication
import configuration
import serialization
import payload

class Commander(object):

	def __init__(self, config = configuration.Config(), serializer = serialization.Serializer(), payload = payload.Payload()):
		
		self.context = zmq.Context()
		self.settings = config
		self.serializer = serializer
		self.payload = payload

		self.controller = communication.connect_socket(self.context, socket_type = zmq.REQ, connection = self.settings.connections["commander"])

		self.logger = logging.getLogger("commander")

	def process(self, args):

		try:

			# split command line arguments
			for arg in vars(args):
				if getattr(args, arg):
					command, argument = arg, getattr(args, arg)
				
			self.logger.info("Command: %s", command)
			
			topic = self.get_topic(command)

			self.logger.info("Topic: %s", topic)
			
			payload = self.payload.read(path=argument,topic=topic)
			self.logger.info("Payload: %s", payload)

			self.send_command(command,payload)

		except Exception as error:
			self.logger.exception("Processing command failed.")
			self.logger.info("Shutting down commander.")
			sys.exit()
			
	def get_topic(self, command):
				
		if command in self.settings.write_commands:
			return self.remove_prefix(command,"write_")
			
		return None

	def send_command(self, command, payload):

		payload_buffer = self.serializer.write_buffer(payload, topic = self.get_topic(command))
		
		self.controller.send("%s %s" % (command, payload_buffer))

		response = self.controller.recv()

		self.logger.debug("Controller executed command: %s", response)
		assert(command == response)
		self.logger.info("Done.")

	def remove_prefix(self, message, prefix):
		
		if message.startswith(prefix):
			return message[len(prefix):]
		return message

def main(args):
	
	commander = Commander()
	commander.process(args)

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
	group.add_argument('-q', '--quit', help='shutdown controller', action='store_true')
	group.add_argument('-p','--pause', help='put controller in idle state and listen for further commands', action='store_true')
	group.add_argument('-rw','--read_weights', action='store_true', help='tell controller to read weights', )
	group.add_argument('-ww','--write_weights', metavar="weight file", nargs='?', const = "config/weights/example.file", help='tell controller to write weights', )
	group.add_argument('-rp','--read_parameters', action='store_true', help='tell controller to read parameters', )
	group.add_argument('-wp','--write_parameters', metavar="parametsr file", nargs='?', const = "config/parameters/example.file", help='tell controller to write parameters', )
	group.add_argument('-rt','--read_topology', action='store_true', help='tell controller to read network topology', )
	group.add_argument('-wt','--write_topology', metavar="topology file", nargs='?', const = "config/topology/example.file", help='tell controller to write network topology', )
	group.add_argument('-rs','--read_spikes', action='store_true', help='tell controller to read neuron spikes', )
	args = parser.parse_args()
	
	main(args)