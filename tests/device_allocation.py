import pyalp as alp


# Allocate device
dev = alp.device.allocate()

# Print device number and identifier
print("  Device number    : {}".format(dev.nb))
print("  Device identifier: {}".format(dev.id))
