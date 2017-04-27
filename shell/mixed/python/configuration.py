import logging

class Config(object):

	def __init__(self):

		self.read_commands = ["read_weights", "read_parameters", "read_spikes", "read_topology"]
		self.write_commands = ["write_weights", "write_parameters", "write_topology"]
		self.topics = {"weights" : "weights", "parameters" : "parameters", "spikes" : "spikes", "topology" : "topology", "camera": "camera" }

		self.connections = {	"commander"	:	"tcp://localhost:5555",
				"controller"	:	"tcp://*:5555",
				"input_data"	:	"tcp://localhost:5556",
				"camera"	:	"tcp://*:5556",
				"output_data"	:	"tcp://localhost:5557",
				"monitor"	:	"tcp://*:5557",
			  }

		self.socket_name = { 6: "zmq.ROUTER", 5: "zmq.DEALER", 4 : "zmq.REP", 3: "zmq.REQ", 2: "zmq.SUB", 1: "zmq.PUB" }
