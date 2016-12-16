import pyalp as alp



# Allocate device
dev = alp.device.allocate()

# Define sequences
seq_1 = alp.sequence.White()
seq_2 = alp.sequence.Black()
seq_3 = alp.sequence.White()
# Define queue
queue = [seq_1, seq_2, seq_3]

# Display queue
dev.display(queue)
