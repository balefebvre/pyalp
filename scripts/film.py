"""Script to play a film at a given frame rate."""

import os

import pyalp as alp


__author__ = "Baptiste Lefebvre"
__copyright__ = "Copyright 2017, Baptiste Lefebvre"
__license__ = "MIT"
__date__ = "2017-08-08"


# Parameters.
bin_pathname = os.path.join("data", "rectangle_f60_a2.30.bin")
vec_pathname = os.path.join("data", "rectangle_f60_a2.30.vec")
rate = 60.0  # frame rate [Hz].

# Check whether files exist.
assert os.path.isfile(bin_pathname)
assert os.path.isfile(vec_pathname)

# Allocate device.
dev = alp.device.allocate_sequence(verbose=True)

# Define stimulus.
stim = alp.stimulus.Film(bin_pathname=bin_pathname, vec_pathname=vec_pathname, rate=rate, verbose=True)

# Display stimulus.
dev.display(stim)
