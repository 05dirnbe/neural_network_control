import logging
import time
import os, sys
import configuration

class Payload_Operations(object):

	def __init__(self):

		self.logger = logging.getLogger("Payload control")

	def prepare_read(self, path):

		time.sleep(1)

		if os.path.isfile(path):

			self.logger.info("File exists: %s", path)

		else:
			self.logger.info("File does not exist: %s", path)
			raise IOError("File not found.")
			
	def prepare_write(self, path):

		time.sleep(1)

		directory = os.path.dirname(path)

		if not os.path.exists(directory):
			self.logger.info("Creating directory: %s", directory)
    		os.makedirs(directory)
		
	def read_weights(self, path):
		self.logger.info("Reading: %s", path)
		return "Payload_weights"

	def read_parameters(self, path):
		self.logger.info("Reading: %s", path)
		return "Payload_parameters"

	def read_topology(self, path):
		self.logger.info("Reading: %s", path)
		return "Payload_topology"

	def dummy_read(self, path):
		self.logger.info("Reading: %s", "dummy.file")
		return "Payload_dummy"

	def write_weights(self, data, path):

		self.logger.info("Writing: %s", path)
		return "Payload_weights"

	def write_parameters(self, data, path):

		self.logger.info("Writing: %s", path)
		return "Payload_parameters"

	def write_topology(self, data, path):

		self.logger.info("Writing: %s", path)
		return "Payload_topology"

	def dummy_write(self, data, path):

		self.logger.info("Writing: %s", path)
		return "Payload_dummy"

class Payload_Adapter(object):

	def __init__(self, operator, config):

		self.logger = logging.getLogger("Payload interface")
		self.settings = config
		self.read_commands = self.settings.read_commands
		self.write_commands = self.settings.write_commands
		self.topics = self.settings.topics

		self.operator = operator
	
class Payload(Payload_Adapter):

	def __init__(self, operator = Payload_Operations(), config=configuration.Config()):

		super(Payload, self).__init__(operator, config)

	def read(self, path, topic=None):

		self.logger.info("Requesting Payload read: %s", topic )
		self.operator.prepare_read(path)

		if topic == "weights":
			return self.operator.read_weights(path)

		if topic == "parameters":
			return self.operator.read_parameters(path)

		if topic == "topology":
			return self.operator.read_topology(path)

		return self.operator.dummy_read(path)

	def write(self, data, path, topic=None):

		self.logger.info("Requesting Payload write: %s", topic )
		self.operator.prepare_write(path)

		if topic == "weights":
			self.operator.write_weights(data, path)
			return

		if topic == "parameters":
			self.operator.write_parameters(data, path)
			return

		if topic == "topology":
			self.operator.write_topology(data, path)
			return

		self.operator.dummy_write(data, path)

