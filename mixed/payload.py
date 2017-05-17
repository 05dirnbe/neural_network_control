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
		
		pass

	def read_matrix(self, path):
		self.logger.debug("Reading: %s", path)
		return np.loadtxt(path, delimiter=',', dtype = int)

	def write_matrix(self, data, path):
		assert isinstance(data, (np.ndarray, np.generic) )
		assert len(data.shape) == 2
		assert data.dtype == int

		self.logger.debug("Writing: %s", path)
		return np.savetxt(path, data , delimiter=',', fmt="%d")

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
			return self.operator.read_matrix(path)

		if topic == "parameters":
			self.logger.debug("Requesting Payload read: %s", topic )
			self.operator.prepare_read(path)
			return self.operator.read_matrix(path)

		if topic == "topology":
			self.logger.debug("Requesting Payload read: %s", topic )
			self.operator.prepare_read(path)
			return self.operator.read_matrix(path)

		return None

	def write(self, data, path, topic=None):

		if topic == "weights":
			self.logger.debug("Requesting Payload write: %s", topic )
			self.operator.prepare_write(path)
			self.operator.write_matrix(data, path)
			pass

		if topic == "parameters":
			self.logger.debug("Requesting Payload write: %s", topic )
			self.operator.prepare_write(path)
			self.operator.write_matrix(data, path)
			pass

		if topic == "topology":
			self.logger.debug("Requesting Payload write: %s", topic )
			self.operator.prepare_write(path)
			self.operator.write_matrix(data, path)
			pass

		