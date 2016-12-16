import pyalp as alp



# Allocate device
dev = alp.device.allocate()

# Define sequence
seq = alp.sequence.BlackWhite()
# Define queue
queue = [seq]

# Display queue
dev.display(queue)
