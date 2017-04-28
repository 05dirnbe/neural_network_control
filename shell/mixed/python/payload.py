import logging
import time
import os, sys
import numpy as np

import configuration

class Payload_Operations(object):

	def __init__(self):

		self.logger = logging.getLogger("Payload control")
		self.logger.setLevel(logging.INFO)

	def prepare_read(self, path):

		time.sleep(1)

		if os.path.isfile(path):

			self.logger.debug("File exists: %s", path)

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
		self.logger.debug("Reading: %s", path)
		return np.loadtxt(path, delimiter=',', dtype = int)

	def read_parameters(self, path):
		self.logger.debug("Reading: %s", path)
		return np.loadtxt(path, delimiter=',', dtype = int)

	def read_topology(self, path):
		self.logger.debug("Reading: %s", path)
		return np.loadtxt(path, delimiter=',', dtype = int)

	def dummy_read(self, path):
		self.logger.debug("Nothing to read ...")
		return None

	def write_weights(self, data, path):

		self.logger.debug("Writing: %s", path)
		return "Payload_weights"

	def write_parameters(self, data, path):

		self.logger.debug("Writing: %s", path)
		return "Payload_parameters"

	def write_topology(self, data, path):

		self.logger.debug("Writing: %s", path)
		return "Payload_topology"

	def dummy_write(self, data, path):

		self.logger.debug("Writing: %s", path)
		return "Payload_dummy"

class Payload_Adapter(object):

	def __init__(self, operator, config):

		self.logger = logging.getLogger("Payload interface")
		self.logger.setLevel(logging.INFO)
		self.settings = config
		self.read_commands = self.settings.read_commands
		self.write_commands = self.settings.write_commands
		self.topics = self.settings.topics

		self.operator = operator
	
class Payload(Payload_Adapter):

	def __init__(self, operator = Payload_Operations(), config=configuration.Config()):

		super(Payload, self).__init__(operator, config)

	def read(self, path, topic=None):

		if topic == "weights":
			self.logger.debug("Requesting Payload read: %s", topic )
			self.operator.prepare_read(path)
			return self.operator.read_weights(path)

		if topic == "parameters":
			self.logger.debug("Requesting Payload read: %s", topic )
			self.operator.prepare_read(path)
			return self.operator.read_parameters(path)

		if topic == "topology":
			self.logger.debug("Requesting Payload read: %s", topic )
			self.operator.prepare_read(path)
			return self.operator.read_topology(path)

		return self.operator.dummy_read(path)

	def write(self, data, path, topic=None):

		if topic == "weights":
			self.logger.debug("Requesting Payload write: %s", topic )
			self.operator.prepare_write(path)
			self.operator.write_weights(data, path)
			return

		if topic == "parameters":
			self.logger.debug("Requesting Payload write: %s", topic )
			self.operator.prepare_write(path)
			self.operator.write_parameters(data, path)
			return

		if topic == "topology":
			self.logger.debug("Requesting Payload write: %s", topic )
			self.operator.prepare_write(path)
			self.operator.write_topology(data, path)
			return

		self.operator.dummy_write(data, path)

