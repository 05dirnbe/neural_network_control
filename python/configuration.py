import logging

class Config(object):

	def __init__(self):

		self.read_commands = ["read_weights", "read_parameters", "read_spikes", "read_topology"]
		self.write_commands = ["write_weights", "write_parameters", "write_topology"]
		self.topics = {"weights" : "weights", "parameters" : "parameters", "spikes" : "spikes", "topology" : "topology", "camera": "camera", "command" : "command" }

		self.desktop_ip = "localhost"
		self.raspberry_ip = "localhost"
		self.ip = self.raspberry_ip

		self.connections = {	"commander"	:	"tcp://" + self.ip + ":5555",
				"controller"	:	"tcp://" + self.ip + ":5555",
				"input_data"	:	"tcp://" + self.ip + ":5556",
				"camera"	:	"tcp://" + self.ip + ":5556",
				"output_data"	:	"tcp://" + self.ip + ":5557",
				"monitor"	:	"tcp://" + self.ip + ":5557",
			  }

		self.socket_name = { 6: "zmq.ROUTER", 5: "zmq.DEALER", 4 : "zmq.REP", 3: "zmq.REQ", 2: "zmq.SUB", 1: "zmq.PUB" }
