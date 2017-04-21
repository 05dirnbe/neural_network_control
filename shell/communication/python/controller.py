import zmq
import logging
from communication import *

def main(context):

    logger = logging.getLogger(__name__)

    commander = bind_socket(context, socket_type = zmq.REP, connection = connections["controller"])
    
    input_data = bind_socket(context, socket_type = zmq.SUB, connection = connections["camera"])
    input_data.setsockopt(zmq.SUBSCRIBE,"")
  
    output_data = bind_socket(context, socket_type = zmq.PUB, connection = connections["monitor"])

    # Initialize poll set
    poller = zmq.Poller()
    poller.register(commander, zmq.POLLIN)
    poller.register(input_data, zmq.POLLIN)

    # Process messages from both sockets
    
    command = None

    while True:
        try:
            socks = dict(poller.poll())
        except KeyboardInterrupt:
            break

        if commander in socks:
            command = commander.recv()
            logger.info("Recieved command: %s", command)
            commander.send(command)
            logger.debug("Acknowledged command: %s", command)
   
        if input_data in socks:
            data = input_data.recv()
            logger.info("Recieved data: %s", data)
       
        if command == "read_weights":
            output_data.send("%s %s" % (topics["weights"], "Weights data"))
            logger.info("Sending data: Weights")

        if command == "read_parameters":
            output_data.send("%s %s" % (topics["parameters"], "Parameters data"))
            logger.info("Sending data: Parameters")

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
