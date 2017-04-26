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

		self.logger.info("Initializing controller ...")
		self.logger.info("Connecting sockets ...")

		self.commander = communication.bind_socket(self.context, socket_type = zmq.REP, connection = self.connections["controller"])
		self.input_data = communication.bind_socket(self.context, socket_type = zmq.SUB, connection = self.connections["camera"])
		self.output_data = communication.bind_socket(self.context, socket_type = zmq.PUB, connection = self.connections["monitor"])
		
		#input subscribes to any topic, i.e. these sockets read from all their connections at once
		self.input_data.setsockopt(zmq.SUBSCRIBE,"")

		self.logger.info("Initializing poll sets ...")
		# Initialize poll set
		self.poller = zmq.Poller()
		self.poller.register(self.commander, zmq.POLLIN)
		self.poller.register(self.input_data, zmq.POLLIN)
		self.logger.info("Initialization complete.")

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
				self.command, payload = self.read_command(self.commander)

			if self.input_data in socks:	
				camera_data = self.read_data(self.input_data, topic="camera")
				self.write_fpga_data(camera_data, topic="camera")

			if self.command:
				self.handle_command(self.command, payload)
				
	def read_command(self, commander):

		message = commander.recv()
		command, payload = message.split()
		self.logger.info("Recieved command: %s", command)
		commander.send(command)
		self.logger.debug("Acknowledged command: %s", command)

		return command, payload
	
	def handle_command(self, command, payload):

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
			self.write_fpga_data(payload, topic=topic)

			return

		return

	def read_fpga_data(self, topic):
		
		return self.FPGA.read(topic = topic)

	def write_fpga_data(self, data, topic):
		
		self.FPGA.write(data, topic = topic)
		self.pause()

	def publish_fpga_data(self, output_data, data, topic):

		self.logger.info("Publishing %s monitor data: %s", topic, data)

		# serialize stuff
		data_buffer = self.serializer.write_buffer(data, topic)

		output_data.send("%s %s" % (self.topics[topic], data_buffer))
		
	def read_camera_data(self, input_data):

		camera_data = input_data.recv()
		self.logger.info("Recieved data: %s", camera_data)
		return camera_data

	def read_data(self, socket, topic):

		data_buffer = socket.recv()
		data = self.serializer.read_buffer(data_buffer,topic=topic)

		self.logger.info("Recieved %s data: %s", topic, data)
		return data
		
	def quit(self):
		self.logger.info("Shutting down controller.")
		sys.exit()

	def pause(self):
		self.logger.info("Pausing operation. Controller waiting for new commands ...")
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
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(name)s: -- %(levelname)s -- %(message)s')
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)

	main()
	
