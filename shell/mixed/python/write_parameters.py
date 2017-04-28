import json
import numpy as np

np.random.seed(0)

path = "config/parameters/example.out"

data = np.random.randint(256, size=5)

np.savetxt(path,data , delimiter=',', fmt="%d")   

print data
print type(data)
print data.dtype