import zmq

raspberry_ip = ""
context = zmq.Context()
channel = '1001'
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, channel)
socket.connect("tcp://"+ raspberry_ip +":5000")
print "socket connected"

while True:
    print "Waiting for message"
    message = socket.recv()
    print "message received: ", message
