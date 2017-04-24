import zmq
import logging
import time
from communication import *

def main(context):

	logger = logging.getLogger(__name__)

	logger.info("Connecting sockets ...")

	commander = bind_socket(context, socket_type = zmq.REP, connection = connections["controller"])
	
	input_data = bind_socket(context, socket_type = zmq.SUB, connection = connections["camera"])
	input_data.setsockopt(zmq.SUBSCRIBE,"")
  
	output_data = bind_socket(context, socket_type = zmq.PUB, connection = connections["monitor"])

	logger.info("Initializing poll sets ...")
	# Initialize poll set
	poller = zmq.Poller()
	poller.register(commander, zmq.POLLIN)
	poller.register(input_data, zmq.POLLIN)

	# Process messages from both sockets
	
	logger.info("Controller ready. Listening for commands ...")

	command = None

	while True:
		
		try:
			time.sleep(0.5)
			socks = dict(poller.poll(0))
		except KeyboardInterrupt:
			break

		if commander in socks:
			command = commander.recv()
			logger.info("Recieved command: %s", command)
			commander.send(command)
			logger.debug("Acknowledged command: %s", command)

		if command == "quit":
			logger.info("Shutting down controller.")
			return

		if command == "pause":
			logger.info("Pausing operation. Controller waiting for commands")
			command = None

		if input_data in socks:
			data = input_data.recv()
			logger.info("Recieved data: %s", data)
	   
		if command == "read_spikes":
			logger.info("Reading FPGA data: Spikes")
			time.sleep(1)
			output_data.send("%s %s" % (topics["spikes"], "Spikes data"))
			logger.info("Sending monitor data: Spikes")

		if command == "read_weights":
			logger.info("Reading FPGA data: Weights")
			time.sleep(1)
			output_data.send("%s %s" % (topics["weights"], "Weights data"))
			logger.info("Sending monitor data: Weights")

		if command == "write_weights":
			time.sleep(1)
			logger.info("Writing FPGA data: Weights")
			command = None

		if command == "read_parameters":
			logger.info("Reading FPGA data: Parameters")
			time.sleep(1)
			output_data.send("%s %s" % (topics["parameters"], "Parameters data"))
			logger.info("Sending monitor data: Parameters")

		if command == "write_parameters":
			time.sleep(1)
			logger.info("Writing FPGA data: Parameters")
			command = None

		if command == "read_topology":
			logger.info("Reading FPGA data: Topology")
			time.sleep(1)
			output_data.send("%s %s" % (topics["topology"], "Network topology"))
			logger.info("Sending monitor data: Topology")

		if command == "write_topology":
			time.sleep(1)
			logger.info("Writing FPGA data: topology")
			command = None

	return 

if __name__ == '__main__':

	# Setup for application logging
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(name)s: -- %(levelname)s -- %(message)s', filename="./log/controller.log", filemode="w")
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(name)s: -- %(levelname)s -- %(message)s')
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)

	# Setup for communication
	context = zmq.Context()

	main(context)
