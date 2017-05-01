import logging
import time
import numpy as np

import configuration

class FPGA_Operations(object):

	def __init__(self):

		self.logger = logging.getLogger("FPGA control")
		self.state = None
		self.parameters = np.zeros(0,dtype=int)
		self.weights = np.zeros((0,0),dtype=int)
		self.topology = np.zeros((0,0),dtype=int)
		self.spikes = np.array([ (0,34), (1, 523)])

	def prepare_read(self):

		time.sleep(1)

		self.state = "write"
		# set read/write bit to read

		self.logger.info("New FPGA state: %s", self.state)

	def prepare_write(self):

		time.sleep(1)

		# set read/write bit to write

		self.state = "write"
		self.logger.info("New FPGA state: %s", self.state)

	def read_weights(self):

		return self.weights

	def read_parameters(self):

		return self.parameters

	def read_spikes(self):

		return self.spikes

	def read_topology(self):

		return self.topology

	def dummy_read(self):

		return "FPGA_dummy"

	def write_weights(self, data):
		self.weights = data
		self.logger.info("Payload is: %s", data)
		return "FPGA_weights"

	def write_parameters(self, data):
		self.parameters = data
		self.logger.info("Payload is: %s", data)
		return "FPGA_parameters"

	def write_spikes(self, data):

		self.logger.info("Payload is: %s", data)
		return "FPGA_spikes"

	def write_topology(self, data):
		self.topology = data
		self.logger.info("Payload is: %s", data)
		return "FPGA_topology"

	def write_camera(self, data):

		self.logger.info("Payload is: %s", data)
		return "FPGA_camera_data"

	def dummy_write(self, data):

		self.logger.info("Payload is: %s", data)
		return "FPGA_dummy"

class FPGA_Adapter(object):

	def __init__(self, operator, config):

		self.logger = logging.getLogger("FPGA interface")
		self.settings = config
		self.read_commands = self.settings.read_commands
		self.write_commands = self.settings.write_commands
		self.topics = self.settings.topics

		self.operator = operator
	
class FPGA(FPGA_Adapter):

	def __init__(self, operator = FPGA_Operations(), config=configuration.Config()):

		super(FPGA, self).__init__(operator, config)

	def read(self, topic=None):

		self.logger.info("Requesting FPGA read: %s", topic )
		self.operator.prepare_read()

		if topic == "weights":
			return self.operator.read_weights()

		if topic == "parameters":
			return self.operator.read_parameters()

		if topic == "spikes":
			return self.operator.read_spikes()

		if topic == "topology":
			return self.operator.read_topology()

		return self.operator.dummy_read()

	def write(self, data, topic=None):

		self.logger.info("Requesting FPGA write: %s", topic )
		self.operator.prepare_write()

		if topic == "weights":
			self.operator.write_weights(data)
			return

		if topic == "parameters":
			self.operator.write_parameters(data)
			return

		if topic == "spikes":
			self.operator.write_spikes(data)
			return

		if topic == "topology":
			self.operator.write_topology(data)
			return

		if topic == "camera":
			self.operator.write_camera(data)
			return

		self.operator.dummy_write(data)

