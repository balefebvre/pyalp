import pyalp as alp



# Allocate device
dev = alp.device.allocate()

# Print device number and identifier
print("Dev nb: {}".format(dev.nb))
print("Dev id: {}".format(dev.id))
