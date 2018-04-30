import pyalp as alp



# Allocate device
dev = alp.device.allocate_sequence()

# Print device number and identifier
print("  Device number    : {}".format(dev.nb))
print("  Device identifier: {}".format(dev.id))
