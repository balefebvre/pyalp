"""Script to play a full-field binary pattern at a given frame rate and for a given duration"""

import pyalp as alp


__author__ = "Baptiste Lefebvre"
__copyright__ = "Copyright 2017, Baptiste Lefebvre"
__license__ = "MIT"
__date__ = "2017-08-04"


# Parameters.
check_size = 18  # px  # check size
nb_checks = 20  # number of checks
rate = 50.0  # 40.0  # Hz  # frame rate
duration = 5.0 * 60.0  # s  # duration

# Allocate device.
dev = alp.device.allocate(verbose=True)

# Define stimulus.
stim = alp.stimulus.Checkerboard(check_size=check_size, nb_checks=nb_checks, rate=rate, duration=duration, verbose=True)

# Print parameters.
print("check size: {}".format(check_size))
print("nb checks: {}".format(nb_checks))
print("rate: {} Hz".format(rate))
print("duration: {} s".format(duration))

# Display stimulus.
dev.display(stim)
