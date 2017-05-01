import json
import numpy as np
from payload import Payload

np.random.seed(0)
payload = Payload()

topic = "topology"
path = "config/topology/example.out"

# prepare the vladimir data here. Call whatever other functions are needed. 
data = np.random.randint(255, size=(2,5))
# write to file using the payload api. Data must be a 2d np array of type int
payload.write(data, path, topic)