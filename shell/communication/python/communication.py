import logging
import configuration

logger = logging.getLogger(__name__)
settings = configuration.Config()

def bind_socket(context, socket_type, connection):

    logger.info("Binding %s socket to: %s", settings.socket_name[socket_type], connection)
    sock = context.socket(socket_type)
    sock.bind(connection)

    return sock

def connect_socket(context, socket_type, connection):

    logger.info("Connecting %s socket to: %s", settings.socket_name[socket_type], connection)
    sock = context.socket(socket_type)
    sock.connect(connection)

    return sock