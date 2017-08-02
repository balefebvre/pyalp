import pyalp as alp


# Allocate device
dev = alp.device.allocate()

# TODO remove following lines.
settings = dev.inquire_settings()
print(settings)
import sys
sys.exit(0)

# Define protocol
pro = alp.protocol.Checkerboard()

# Display protocol
dev.display(pro)
