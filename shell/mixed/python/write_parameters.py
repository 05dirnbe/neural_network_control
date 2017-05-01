import json
import numpy as np
import payload

np.random.seed(0)
payload = payload.Payload()

topic = "parameters"
path = "config/parameters/example.out"

# prepare the vladimir data here. Call whatever other functions are needed. 
data = np.random.randint(256, size=5)
# write to file using the payload api. Data must be a 1d np array of type int
payload.write(data, path, topic)
