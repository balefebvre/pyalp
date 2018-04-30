import pyalp as alp


# Allocate device
dev = alp.device.allocate_sequence_bis(verbose=True)

# Define stimulus
rate = 10100.0  # Hz
duration = 5.0  # s
nb_repetitions = int(rate * duration)
stim = alp.stimulus.FullFieldBinaryPattern(rate=rate, nb_repetitions=nb_repetitions)

print("rate: {} Hz".format(rate))
print("picture time: {} ms".format(1.0e+3 / rate))
print("")

# Display stimulus
dev.display(stim)
