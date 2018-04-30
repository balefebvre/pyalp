import pprint
import pyalp as alp



# Allocate device
dev = alp.device.allocate_sequence_bis()

# Inquire device settings
settings = dev.inquire_settings()

# Print device settings
print("Device's settings:")
pprint.pprint(settings)
