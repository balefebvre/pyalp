import pyalp as alp


# Allocate device
dev = alp.device.allocate_sequence_bis()

# Define stimulus
stim = alp.stimulus.Film()

# Display stimulus
dev.display(stim)
