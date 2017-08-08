"""Script to play a film at a given frame rate."""

import pyalp as alp


__author__ = "Baptiste Lefebvre"
__copyright__ = "Copyright 2017, Baptiste Lefebvre"
__license__ = "MIT"
__date__ = "2017-08-08"


# Parameters.
bin_pathname = ""  # TODO correct.
vec_pathname = ""  # TODO correct.
rate = 40.0  # frame rate [Hz].

# Allocate device.
dev = alp.device.allocate(verbose=True)

# Define stimulus.
stim = alp.stimulus.Film(bin_pathname=bin_pathname, vec_pathname=vec_pathname, rate=rate)

# Display stimulus.
dev.display(stim)
