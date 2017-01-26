import pyalp as alp



# Allocate device
dev = alp.device.allocate()

# Define protocol
pro = alp.protocol.BlackWhite()

# Display protocol
dev.display(pro)
