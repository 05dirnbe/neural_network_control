import zmq
import logging
import time, sys

import communication
import configuration
import serialization
import fpga

class Controller(object):

	def __init__(self, config = configuration.Config(), FPGA = fpga.FPGA(), serializer = serialization.Serializer()):

		self.context = zmq.Context()
		self.settings = config
		self.FPGA = FPGA
		self.serializer = serializer
		
		self.connections = self.settings.connections
		self.read_commands = self.settings.read_commands
		self.write_commands = self.settings.write_commands
		self.topics = self.settings.topics

		self.logger = logging.getLogger("controller")

		self.logger.debug("Initializing controller ...")
		self.logger.debug("Connecting sockets ...")

		self.commander = communication.bind_socket(self.context, socket_type = zmq.REP, connection = self.connections["controller"])
		self.input_data = communication.bind_socket(self.context, socket_type = zmq.SUB, connection = self.connections["camera"])
		self.output_data = communication.bind_socket(self.context, socket_type = zmq.PUB, connection = self.connections["monitor"])
		
		#input subscribes to any topic, i.e. these sockets read from all their connections at once
		self.input_data.setsockopt(zmq.SUBSCRIBE,"")

		self.logger.debug("Initializing poll sets ...")
		# Initialize poll set
		self.poller = zmq.Poller()
		self.poller.register(self.commander, zmq.POLLIN)
		self.poller.register(self.input_data, zmq.POLLIN)
		self.logger.debug("Initialization complete.")

		self.command = None
		
	def serve_forever(self):

		self.logger.info("Controller ready. Listening for commands ...")
		
		while True:
		
			try:
				time.sleep(0.5)
				socks = dict(self.poller.poll(0))
			except KeyboardInterrupt:
				break

			if self.commander in socks:		
				self.command, payload_buffer = self.read_command(self.commander)

			if self.input_data in socks:
				self.logger.debug("--------------- Handling Camera data --------------------")
				camera_data = self.read_data(self.input_data, topic="camera")
				self.write_fpga_data(camera_data, topic="camera")

			if self.command:
				self.logger.debug("--------------- Handling Command --------------------")
				self.handle_command(self.command, payload_buffer)
				
	def read_command(self, commander):

		message = commander.recv()
		command_buffer, payload_buffer = message.split(" ", 1)

		command = self.serializer.read_buffer(command_buffer, topic = "command")
		command_buffer = self.serializer.write_buffer(command, topic = self.settings.topics["command"])
		commander.send(command_buffer)

		self.logger.info("Recieved command: %s", command)
				
		return command, payload_buffer
	
	def handle_command(self, command, payload_buffer):

		def remove_prefix(message, prefix):
			if message.startswith(prefix):
				return message[len(prefix):]
			return message

		# handle easy cases immediately
		if command == None:		return
		if command == "quit":	self.quit()
		if command == "pause": 	self.pause()

		if command in self.settings.read_commands:

			topic = remove_prefix(command,"read_")
			data = self.read_fpga_data(topic=topic)
			self.publish_fpga_data(self.output_data, data, topic=topic)

			return

		if command in self.settings.write_commands:

			topic = remove_prefix(command,"write_")
			payload = self.serializer.read_buffer(payload_buffer, topic=topic)
			self.write_fpga_data(payload, topic=topic)

			return

		return

	def read_fpga_data(self, topic):
		
		self.logger.debug("Reading %s FPGA data", topic)
		return self.FPGA.read(topic = topic)

	def write_fpga_data(self, data, topic):
		
		self.logger.info("Writing %s FPGA data: %s", topic, data)
		self.FPGA.write(data, topic = topic)
		self.pause()

	def publish_fpga_data(self, output_data, data, topic):

		self.logger.info("Publishing %s monitor data: %s", topic, data)

		# serialize stuff
		data_buffer = self.serializer.write_buffer(data, topic)

		message = topic + " " + data_buffer
		output_data.send(message)
		
	def read_data(self, socket, topic):

		data_buffer = socket.recv()
		data = self.serializer.read_buffer(data_buffer,topic=topic)
		assert type(data) == int
		self.logger.debug("Recieved %s data: %s", topic, data)
		return data
		
	def quit(self):
		self.logger.info("Shutting down controller.")
		sys.exit()

	def pause(self):
		self.logger.debug("Controller waiting for next command ...")
		self.command = None

def main():

	try:
		controller = Controller()
		controller.serve_forever()
	except Exception as e:
		logging.exception("Something bad happened in the controller. You might want to check the log in /log/controller.log")

if __name__ == '__main__':

	# Setup for application logging
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(name)s: -- %(levelname)s -- %(message)s', filename="./log/controller.log", filemode="w")
	console = logging.StreamHandler()
	console.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(name)s: -- %(levelname)s -- %(message)s')
	console.setFormatter(formatter)
	logging.getLogger("controller").addHandler(console)

	main()
	
