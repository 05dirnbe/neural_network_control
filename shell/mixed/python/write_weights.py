import json
import numpy as np

np.random.seed(0)

path = "config/weights/example.out"

data = np.random.randint(255, size=(2,5))

print data
print data.shape

np.savetxt(path,data , delimiter=',', fmt="%d")   


a = np.loadtxt(path, delimiter=',', dtype = int)
