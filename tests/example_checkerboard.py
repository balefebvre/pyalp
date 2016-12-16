import pyalp as alp



# Allocate device
dev = alp.device.allocate()

# Define protocol
pro = alp.protocol.Checkerboard()

# Display protocol
dev.display(protocol)
