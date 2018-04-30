import pyalp as alp



# Allocate device
dev = alp.device.allocate_sequence_bis()

# Define protocol
pro = alp.protocol.MovingBar()

# Display protocol
dev.display(protocol)
