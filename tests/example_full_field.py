import numpy

import pyalp as alp



# Create footprint array
k = 3
theta_min = - (2 * k + 1) * numpy.pi
theta_max = + (2 * k + 1) * numpy.pi
theta = numpy.linspace(theta_min, theta_max, num=10000)
footprint_array = 255.0 * (numpy.cos(theta) + 1.0)
footprint_array = footprint_array.astype('uint8')

# Allocate device
dev = alp.device.allocate()

# Define sequence
seq = alp.sequence.FullField(footprint_array)
# Define queue
queue = [seq]

# Display queue
dev.display(queue)
