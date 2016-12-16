import pyalp as alp



# Allocate device
dev = alp.device.allocate()

# Define sequence
seq = alp.sequence.White()
# Define queue
queue = [seq]

# Display queue
dev.display(queue)
