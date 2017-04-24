import zmq
import logging
import time, sys

import communication
import configuration

class Controller(object):

	def __init__(self, config = configuration.Config()):

		self.context = zmq.Context()
		self.settings = config
		
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
		
		#input subscribes to any topic, i.e. this socket reads from all sources of input data at once
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
				self.command = self.read_command(self.commander)

			if self.input_data in socks:	
				camera_data = self.read_camera_data(self.input_data)

			self.handle_command(self.command)
				
	def read_command(self, commander):
		
		command = commander.recv()
		self.logger.info("Recieved command: %s", command)
		commander.send(command)
		self.logger.debug("Acknowledged command: %s", command)

		return command
	
	def handle_command(self, command):

		def remove_prefix(text, prefix):
			if text.startswith(prefix):
				return text[len(prefix):]
			return text

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
			data = self.read_data(self.commander, topic = topic)
			self.write_fpga_data(data, topic=topic)

			return

		return

	def read_fpga_data(self, topic):
		
		self.logger.info("Reading FPGA data: %s", topic )

		# fpga helper
		# data = self.FPGA.read(topic = self.topics[topic])

		data =  "data"
		time.sleep(1)

		return data

	def write_fpga_data(self, data, topic):
		
		self.logger.info("Writing FPGA data: %s", topic )

		# fpga helper
		# self.FPGA.write(data, topic = self.topics[topic])

		time.sleep(1)

		self.pause()

	def publish_fpga_data(self, output_data, data, topic):

		self.logger.info("Publishing %s monitor data: %s", topic, data)

		# serialize stuff
		# buf = self.serializer.write_buffer(data, topic)

		output_data.send("%s %s" % (self.topics[topic], data))
		
	def read_camera_data(self, input_data):

		camera_data = input_data.recv()
		self.logger.info("Recieved data: %s", camera_data)
		return camera_data

	def read_data(self, socket, topic):

		# buf = socket.recv()
		# data = self.serializer.deserialize(buf,topic=topic)

		data = "data"

		self.logger.info("Recieved %s data: %s", topic, data)
		return data
		
	def read_camera_data(self, input_data):

		camera_data = input_data.recv()
		self.logger.info("Recieved data: %s", camera_data)
		return camera_data

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
	
