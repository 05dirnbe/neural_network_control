import zmq
import logging
from communication import *

def main(context):

    logger = logging.getLogger(__name__)

    commander = bind_socket(context, socket_type = zmq.REP, connection = connections["controller"])

    # # Connect to weather server
    # subscriber = context.socket(zmq.SUB)
    # subscriber.connect("tcp://localhost:5556")
    # subscriber.setsockopt(zmq.SUBSCRIBE, b"10001")

    # Initialize poll set
    poller = zmq.Poller()
    poller.register(commander, zmq.POLLIN)
    # poller.register(subscriber, zmq.POLLIN)

    # Process messages from both sockets
    while True:
        try:
            socks = dict(poller.poll())
        except KeyboardInterrupt:
            break

        if commander in socks:
            message = commander.recv()
            logger.info("Recieved command: %s", message)
            commander.send(message)
            logger.info("Acknowledged command: %s", message)
            # process task

        # if subscriber in socks:
        #     message = subscriber.recv()
        #     # process weather update

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
