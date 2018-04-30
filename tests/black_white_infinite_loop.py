import pyalp as alp



# Allocate device
dev = alp.device.allocate_sequence()

# Define protocol
pro = alp.protocol.BlackWhite(infinite_loop=True)

# Display protocol
dev.display(pro)
