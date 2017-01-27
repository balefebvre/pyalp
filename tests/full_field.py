import numpy

import pyalp as alp



# Create footprint array
theta_min = -1.0 * numpy.pi
theta_max = +1.0 * numpy.pi
theta = numpy.linspace(theta_min, theta_max, num=100)
footprint_array = 255.0 * 0.5 * (numpy.cos(theta) + 1.0)
# footprint_array = 125.0 * numpy.ones_like(theta)
footprint_array = footprint_array.astype('uint8')

import matplotlib.pyplot as plt
plt.figure()
plt.plot(footprint_array)
plt.show()

# Allocate device
dev = alp.device.allocate()

# Define protocol
pro = alp.protocol.FullField(footprint_array)

# Display protocol
dev.display(pro)
