import logging
from collections import defaultdict
import numpy as np
import flatbuffers

import configuration

import Buffers.Integer
import Buffers.IntegerArray
import Buffers.IntegerMatrix
import Buffers.Spike
import Buffers.SpikesArray
import Buffers.String


class Serializer_Operations(object):

	def __init__(self):

		self.logger = logging.getLogger("serializer")
		self.logger.setLevel(logging.DEBUG)
		
	def deserialize_matrix(self, data_buffer, initial_buffer_size = 0):
		# deserialize flatbuffer into numpy matrix of ints
		assert type(data_buffer) == str

		container = Buffers.IntegerMatrix.IntegerMatrix.GetRootAsIntegerMatrix(data_buffer, initial_buffer_size)

		flat_matrix = np.array([ container.List(i) for i in xrange(container.ListLength()) ])
		data = flat_matrix.reshape(container.N(),container.M())

		self.logger.debug("Deserializing to obtain: %s", data)
		return data

	def deserialize_command(self, data_buffer, initial_buffer_size = 0):
		# deserialize flattbuffer into string
		assert type(data_buffer) == str

		self.logger.debug("Deserializing to obtain: %s", data_buffer)
		return data_buffer

	def serialize_matrix(self, data, initial_buffer_size = 1024):
		# serialize numpy 2d array of ints to flatbuffer
		assert isinstance(data, (np.ndarray, np.generic) )
		assert len(data.shape) == 2
		assert data.dtype == int

		n, m = data.shape
		flat_matrix = data.flatten()

		# Serialize the FlatBuffer data.
		# Note: Since we prepend the items, this loop iterates in reverse order.
		builder = flatbuffers.Builder(initial_buffer_size)
		Buffers.IntegerMatrix.IntegerMatrixStartListVector(builder, len(flat_matrix))
		for value in reversed(flat_matrix):
			builder.PrependUint32(value)
		data = builder.EndVector(len(flat_matrix))

		Buffers.IntegerMatrix.IntegerMatrixStart(builder)

		Buffers.IntegerMatrix.IntegerMatrixAddN(builder, n)
		Buffers.IntegerMatrix.IntegerMatrixAddM(builder, m)
		Buffers.IntegerMatrix.IntegerMatrixAddList(builder, data)
		l = Buffers.IntegerMatrix.IntegerMatrixEnd(builder)

		builder.Finish(l)

		data_buffer = builder.Output()

		return data_buffer

	def serialize_command(self, data, initial_buffer_size = 1024):
		# turn string representation of command to flatbuffer
		assert type(data) == str
		
		return data

class Serializer_Adapter(object):

	def __init__(self, operator, config):

		self.logger = logging.getLogger("serialization")
		self.logger.setLevel(logging.DEBUG)
		self.settings = config
		self.read_commands = self.settings.read_commands
		self.write_commands = self.settings.write_commands
		self.topics = self.settings.topics

		self.operator = operator
	
class Serializer(Serializer_Adapter):

	def __init__(self, operator = Serializer_Operations(), config=configuration.Config()):

		super(Serializer, self).__init__(operator, config)

	def read_buffer(self, data_buffer, topic=None):

		self.logger.debug("Deserialzing topic: %s", topic )
		
		if topic == "weights":
			return self.operator.deserialize_matrix(data_buffer)

		if topic == "parameters":
			return self.operator.deserialize_matrix(data_buffer)

		if topic == "spikes":
			return self.operator.deserialize_matrix(data_buffer)

		if topic == "topology":
			return self.operator.deserialize_matrix(data_buffer)

		if topic == "camera":
			return self.operator.deserialize_matrix(data_buffer)

		if topic == "command":
			return self.operator.deserialize_command(data_buffer)

		else:
			return data_buffer

	def write_buffer(self, data, topic=None):

		self.logger.debug("Serializing topic: %s", topic )
		
		if topic == "weights":
			return self.operator.serialize_matrix(data)
			
		if topic == "parameters":
			return self.operator.serialize_matrix(data)
			
		if topic == "spikes":
			return self.operator.serialize_matrix(data)
			
		if topic == "topology":
			return self.operator.serialize_matrix(data)
			
		if topic == "camera":
			return self.operator.serialize_matrix(data)

		if topic == "command":
			return self.operator.serialize_command(data)

		else:
			return "None"		

