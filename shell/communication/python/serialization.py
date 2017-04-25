import logging
import configuration

class Serializer_Operations(object):

	def __init__(self):

		self.logger = logging.getLogger("operator")
		
	def deserialize_weights(self, data_buffer):
		data = data_buffer
		return data

	def deserialize_parameters(self, data_buffer):
		data = data_buffer
		return data

	def deserialize_spikes(self, data_buffer):
		data = data_buffer
		return data

	def deserialize_topology(self, data_buffer):
		data = data_buffer
		return data

	def dummy_deserialize(self, data_buffer):
		data = data_buffer
		return "deserialize_dummy"

	def serialize_weights(self, data):
		data_buffer = data
		self.logger.info("Serializing: %s", data)
		return data_buffer

	def serialize_parameters(self, data):
		data_buffer = data
		self.logger.info("Serializing: %s", data)
		return data_buffer

	def serialize_spikes(self, data):
		data_buffer = data
		self.logger.info("Serializing: %s", data)
		return data_buffer

	def serialize_topology(self, data):
		data_buffer = data
		self.logger.info("Serializing: %s", data)
		return data_buffer

	def serialize_camera(self, data):
		data_buffer = data
		self.logger.info("Serializing: %s", data)
		return data_buffer

	def dummy_serialize(self, data):
		data_buffer = data
		self.logger.info("Serializing: %s", data)
		return "serialize_dummy"

class Serializer_Adapter(object):

	def __init__(self, operator, config):

		self.logger = logging.getLogger("serialization")
		self.settings = config
		self.read_commands = self.settings.read_commands
		self.write_commands = self.settings.write_commands
		self.topics = self.settings.topics

		self.operator = operator
	
class Serializer(Serializer_Adapter):

	def __init__(self, operator = Serializer_Operations(), config=configuration.Config()):

		super(Serializer, self).__init__(operator, config)

	def read_buffer(self, data_buffer, topic=None):

		self.logger.info("Deserialzing topic: %s", topic )
		
		if topic == "weights":
			return self.operator.deserialize_weights(data_buffer)

		if topic == "parameters":
			return self.operator.deserialize_parameters(data_buffer)

		if topic == "spikes":
			return self.operator.deserialize_spikes(data_buffer)

		if topic == "topology":
			return self.operator.deserialize_topology(data_buffer)

		if topic == "camera":
			return self.operator.deserialize_topology(data_buffer)

		return self.operator.dummy_deserialize(data_buffer)

	def write_buffer(self, data, topic=None):

		self.logger.info("Serializing topic: %s", topic )
		
		if topic == "weights":
			return self.operator.serialize_weights(data)
			
		if topic == "parameters":
			return self.operator.serialize_parameters(data)
			
		if topic == "spikes":
			return self.operator.serialize_spikes(data)
			
		if topic == "topology":
			return self.operator.serialize_topology(data)
			
		if topic == "camera":
			return self.operator.serialize_camera(data)
			
		return self.operator.dummy_serialize(data)

