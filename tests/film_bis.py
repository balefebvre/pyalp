import pyalp as alp



# Allocate device
dev = alp.device.allocate()

# Define stimulus
stim = alp.stimulus.Film()

# Display stimulus
dev.display(stim)