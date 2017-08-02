import pyalp as alp


# Allocate device
dev = alp.device.allocate(verbose=True)

# Define protocol
pro = alp.protocol.Checkerboard()

# Display protocol
dev.display(pro)
