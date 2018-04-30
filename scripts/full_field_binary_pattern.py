"""Script to play a full-field binary pattern at a given frame rate and for a given duration"""

# import os

import pyalp as alp


__author__ = "Baptiste Lefebvre"
__copyright__ = "Copyright 2017, Baptiste Lefebvre"
__license__ = "MIT"
__date__ = "2017-08-04"


# Parameters.
pattern = [True, False]  # binary pattern
# or  # pattern = [1, 0]  # binary pattern
# or  # pattern = [255, 0]  # binary pattern
# or  # pattern = os.path.join("data", "full_field_binary_pattern.csv")  # binary pattern
rate = 1.0e+3  # Hz  # frame rate
duration = 5.0  # s  # duration

# Allocate device.
dev = alp.device.allocate_sequence(verbose=True)

# Define stimulus.
nb_repetitions = int(rate * duration)
stim = alp.stimulus.FullFieldBinaryPattern(pattern=pattern, rate=rate, nb_repetitions=nb_repetitions)

# Print parameters.
print("rate: {} Hz".format(rate))
print("picture time: {} ms".format(1.0e+3 / rate))
print("duration: {} s".format(duration))
print("nb_repetitions: {}".format(nb_repetitions))

# Display stimulus.
dev.display(stim)
