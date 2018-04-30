import pyalp as alp



# Allocate device
dev = alp.device.allocate_sequence_bis()

# Define protocol
pro = alp.protocol.White(nb_repetitions=100)

# Display protocol
dev.display(pro)
