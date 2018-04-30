import pyalp as alp



# Allocate device
dev = alp.device.allocate_sequence()

# Define protocol
pro = alp.protocol.Film()

# Display protocol
dev.display(pro)