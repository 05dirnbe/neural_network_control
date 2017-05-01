import numpy as np
import os, sys

import configuration
import payload


class TopicalWriter(object):

	def __init__(self, topic, config_folder = "config", settings = configuration.Config(), payload = payload.Payload()):

		self.settings = settings
		self.payload = payload
		self.topic = topic
		self.config_folder = config_folder

		self.write_topics = ["weights", "parameters", "topology"]

		if not topic in self.write_topics:
			print "Selected topic not implemented for writing."
			sys.exit()


class TopologyWriter(TopicalWriter):

	def __init__(self, config_folder = "config",  settings = configuration.Config(), payload = payload.Payload()):

		super(TopologyWriter, self).__init__("topology", config_folder, settings, payload)

		self.path = os.path.join(self.config_folder, self.topic)
		
	def prepare_data(self):

		# here all the valdimir code goes creating the topology data for the configuration file
		# returned data must be any 2d numpy array of type int

		np.random.seed(0)
		return np.random.randint(255, size=(2,5))

	def write(self, filename):

		path = os.path.join(self.path, filename)
		data = self.prepare_data()

		self.payload.write(data, path, self.topic)

class WeightsWriter(TopicalWriter):

	def __init__(self, config_folder = "config",  settings = configuration.Config(), payload = payload.Payload()):

		super(WeightsWriter, self).__init__("weights", config_folder, settings, payload)

		self.path = os.path.join(self.config_folder, self.topic)
		
	def prepare_data(self):

		# here all the valdimir code goes creating the topology data for the configuration file
		# returned data must be any 2d numpy array of type int

		np.random.seed(1)
		return np.random.randint(255, size=(2,5))

	def write(self, filename):

		path = os.path.join(self.path, filename)
		data = self.prepare_data()

		self.payload.write(data, path, self.topic)

class ParametersWriter(TopicalWriter):

	def __init__(self, config_folder = "config",  settings = configuration.Config(), payload = payload.Payload()):

		super(ParametersWriter, self).__init__("weights", config_folder, settings, payload)

		self.path = os.path.join(self.config_folder, self.topic)
		
	def prepare_data(self):

		# here all the valdimir code goes creating the topology data for the configuration file
		# returned data must be any 1d numpy array of type int

		np.random.seed(0)
		return np.random.randint(256, size=5)

	def write(self, filename):

		path = os.path.join(self.path, filename)
		data = self.prepare_data()

		self.payload.write(data, path, self.topic)


