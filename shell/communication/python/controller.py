import zmq
import logging
from communication import *

def main(context):

    logger = logging.getLogger(__name__)

    commander = bind_socket(context, socket_type = zmq.REP, connection = connections["controller"])
    input_data = bind_socket(context, socket_type = zmq.SUB, connection = connections["input_data"])
    input_data.setsockopt(zmq.SUBSCRIBE,"")
   
    # Initialize poll set
    poller = zmq.Poller()
    poller.register(commander, zmq.POLLIN)
    poller.register(input_data, zmq.POLLIN)

    # Process messages from both sockets
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
