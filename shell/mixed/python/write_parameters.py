import json
import numpy as np
import payload

np.random.seed(0)
payload = payload.Payload()

topic = "parameters"
path = "config/parameters/example.out"

# prepare data here. Data must be a np array of type int
data = np.random.randint(256, size=5)
# write to file using the payload api
payload.write(data, path, topic)
