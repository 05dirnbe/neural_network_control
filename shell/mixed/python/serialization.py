import logging
import numpy as np
import flatbuffers

import configuration

import Buffers.Integer
import Buffers.IntegerArray
import Buffers.IntegerMatrix
import Buffers.SpikesArray
import Buffers.String


class Serializer_Operations(object):

	def __init__(self):

		self.logger = logging.getLogger("serializer")
		self.logger.setLevel(logging.DEBUG)
		
	def deserialize_weights(self, data_buffer):
		
		return self.deserialize_topology(data_buffer)

	def deserialize_parameters(self, data_buffer):
		# recieve a flatbuffer and deserialize it into an numpy array of ints
		assert type(data_buffer) == str
	
		array = Buffers.IntegerArray.IntegerArray.GetRootAsIntegerArray(data_buffer, 0)
		# Get and test the `values` FlatBuffer `vector`.
		data = np.zeros(array.ListLength(), dtype = int)
		for i in xrange(array.ListLength()):
			data[i] = array.List(i)

		self.logger.debug("Deserializing to obtain: %s", data)
		return data

	def deserialize_spikes(self, data_buffer):
		data = data_buffer
		self.logger.debug("Deserializing to obtain: %s", data)
		return data

	def deserialize_topology(self, data_buffer):
		# deserialize flatbuffer into numpy matrix of ints
		assert type(data_buffer) == str

		try:

			container = Buffers.IntegerMatrix.IntegerMatrix.GetRootAsIntegerMatrix(data_buffer, 0)

			flat_matrix = np.array([ container.List(i) for i in xrange(container.ListLength()) ])
			data = flat_matrix.reshape(container.N(),container.M())

		except Exception as e:
			print e

		self.logger.debug("Deserializing to obtain: %s", data)
		return data

	def deserialize_camera(self, data_buffer):
		# recieve a flatbuffer and deserialize it into an int
		assert type(data_buffer) == str
		
		integer = Buffers.Integer.Integer.GetRootAsInteger(data_buffer, 0)
		data = integer.Value()

		self.logger.debug("Deserializing to obtain: %s", data)
		return data

	def deserialize_command(self, data_buffer):
		# deserialize flattbuffer into string
		assert type(data_buffer) == str

		string = Buffers.String.String.GetRootAsString(data_buffer, 0)
		data = string.Message()

		self.logger.debug("Deserializing to obtain: %s", data)
		return data

	def dummy_deserialize(self, data_buffer):
		
		if data_buffer == "None":
			return None

		self.logger.debug("Deserializing to obtain: %s", data)
		return data

	def serialize_weights(self, data):

		return  self.serialize_topology(data)

	def serialize_parameters(self, data):
		# turn list an np array of ints into flatbuffer
		print data.dtype
		assert isinstance(data, (np.ndarray, np.generic) )
		assert data.dtype == int
		
		n = len(data)

		builder = flatbuffers.Builder(0)
		Buffers.IntegerArray.IntegerArrayStartListVector(builder, n)
		# Note: Since we prepend the items, this loop iterates in reverse order.
		for i in reversed(xrange(n)):
			builder.PrependUint32(data[i])
		l = builder.EndVector(n)

		Buffers.IntegerArray.IntegerArrayStart(builder)
		Buffers.IntegerArray.IntegerArrayAddList(builder, l)
		l = Buffers.IntegerArray.IntegerArrayEnd(builder)
		builder.Finish(l)

		data_buffer = builder.Output()

		self.logger.debug("Serializing: %s", data)

		return data_buffer

	def serialize_spikes(self, data):
		
		
		self.logger.debug("Serializing: %s", data)
		return data_buffer

	def serialize_topology(self, data):
		# serialize numpy 2d array of ints to flatbuffer
		assert isinstance(data, (np.ndarray, np.generic) )
		assert len(data.shape) == 2
		assert data.dtype == int

		n, m = data.shape
		flat_matrix = data.flatten()

		# Serialize the FlatBuffer data.
		# Note: Since we prepend the items, this loop iterates in reverse order.
		builder = flatbuffers.Builder(0)
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

		self.logger.debug("Serializing: %s", data)
		return data_buffer

	def serialize_camera(self, data):
		# here we want to serialize an int to a flatbuffer
		assert type(data) == int
		self.logger.debug("Serializing: %d", data)

		builder = flatbuffers.Builder(0)
		Buffers.Integer.IntegerStart(builder)
		Buffers.Integer.IntegerAddValue(builder,data)
		integer = Buffers.Integer.IntegerEnd(builder)
		
		builder.Finish(integer)
		data_buffer = builder.Output()

		return data_buffer

	def serialize_command(self, data):
		# turn string representation of command to flatbuffer
		assert type(data) == str
		
		self.logger.debug("Serializing: %s", data)

		builder = flatbuffers.Builder(0)
		message = builder.CreateString(data)

		Buffers.String.StringStart(builder)
		Buffers.String.StringAddMessage(builder,message)
		string = Buffers.String.StringEnd(builder)
		builder.Finish(string)

		data_buffer = builder.Output()

		return data_buffer

	def dummy_serialize(self, data):
		data_buffer = "None"
		self.logger.debug("Serializing: %s", data_buffer)
		return data_buffer

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
			return self.operator.deserialize_weights(data_buffer)

		if topic == "parameters":
			return self.operator.deserialize_parameters(data_buffer)

		if topic == "spikes":
			return self.operator.deserialize_spikes(data_buffer)

		if topic == "topology":
			return self.operator.deserialize_topology(data_buffer)

		if topic == "camera":
			return self.operator.deserialize_camera(data_buffer)

		if topic == "command":
			return self.operator.deserialize_command(data_buffer)

		return self.operator.dummy_deserialize(data_buffer)

	def write_buffer(self, data, topic=None):

		self.logger.debug("Serializing topic: %s", topic )
		
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

		if topic == "command":
			return self.operator.serialize_command(data)

		return self.operator.dummy_serialize(data)

