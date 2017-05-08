import time
import zmq

desktop_ip = "*"

context = zmq.Context()
socket = context.socket(zmq.PUB)
print "socket created"
socket.bind("tcp://"+ desktop_ip + ":5000")
print "socket connected"

channel = '1001'
i = 0
while True:
    message = 'Hello %s' % i
    socket.send("%s %s" % (channel, message))
    print "Published: %s " % message
    time.sleep(1)
    i += 1

print "About to close socket"
socket.close()
print "Socket closed"