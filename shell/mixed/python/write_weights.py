import json
import numpy as np
from payload import Payload

np.random.seed(0)
payload = Payload()

topic = "weights"
path = "config/weights/example.out"

# prepare data here. Data must be a np array of type int
data = np.random.randint(255, size=(2,5))
# write to file using the payload api
payload.write(data, path, topic)