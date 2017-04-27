import json
import numpy as np

np.random.seed(0)

path = "config/parameters/parameters.out"

data = np.random.randint(256, size=256)

np.savetxt(path,data , delimiter=',', fmt="%d")   # X is an array


s = bytearray(data.tolist())

message = "command" + " %s" % s

print type(message)

command, payload = message.split(" ", 1)

print command
print type(payload)
print list(payload)