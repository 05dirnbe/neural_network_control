
import logging, sys, time, os
import zmq
import communication
import configuration
import serialization

class TopicalMonitor(object):

	def __init__(self, topic, sleep = 0, connection = "output_data" , settings = configuration.Config(), serializer = serialization.Serializer()):

		self.context = zmq.Context()
		self.settings = settings
		self.serializer = serializer
		self.sleep = sleep
		self.topic = topic

		self.logger_parent = logging.getLogger("topical monitor")
		self.logger_parent.setLevel(logging.INFO)

		self.data = communication.connect_socket(self.context, socket_type = zmq.SUB, connection = self.settings.connections[connection])
		self.data.setsockopt(zmq.SUBSCRIBE, self.settings.topics[topic])

	def serve_forever(self):

		try:

			while True:
				
				topic, data_buffer = self.data.recv().split(" ", 1)
				data = self.serializer.read_buffer(data_buffer, topic = topic)

				self.logger_parent.debug("Recieved: %s", data)
				self.handle(data)
				time.sleep(self.sleep)
								
		except Exception as e:
			self.logger_parent.exception("Listening failed.")
			self.logger_parent.info("Shutting down monitor.")
			sys.exit()

		except KeyboardInterrupt as e:
			self.logger_parent.info("User interrupt.")
			self.logger_parent.info("Shutting down monitor.")
			sys.exit()

	def handle(self, data):

		pass

class FileLogger(TopicalMonitor):

	def __init__(self, topic, path, sleep = 0, connection = "output_data" , settings = configuration.Config(), serializer = serialization.Serializer()):

		super(FileLogger, self).__init__(topic, sleep , connection, settings, serializer)

		self.logger = logging.getLogger(topic + " logger")
		self.logger.setLevel(logging.DEBUG)

		self.folder = os.path.join(path, topic)
		self.log_file = os.path.join(self.folder, topic+"_store"+".txt")

		self.prepare_save(self.folder)

		self.store = open(self.log_file, "w")

		self.logger.info("Starting to log %s to file: %s", self.topic, self.log_file)

	def prepare_save(self, folder):

		if not os.path.exists(folder):
			self.logger.info("Creating directory: %s", folder)
			os.makedirs(folder)

	def handle(self, data):

		self.store.write(data+"\n")
		self.logger.debug("Writing: %s", data)

class Monitor(TopicalMonitor):

	def __init__(self, topic, sleep = 0, connection = "output_data" , settings = configuration.Config(), serializer = serialization.Serializer()):

		super(Monitor, self).__init__(topic, sleep , connection, settings, serializer)

		self.logger = logging.getLogger(topic + " monitor")
		self.logger.setLevel(logging.DEBUG)

		self.logger.info("Starting to monitor: %s", self.topic)

	def handle(self, data):

		self.logger.debug("Plotting: %s", data)