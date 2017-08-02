import pyalp as alp


# Allocate device
dev = alp.device.allocate(verbose=True)

# Define stimulus
stim = alp.stimulus.FullFieldBinaryPattern()

# Display stimulus
dev.display(stim)
