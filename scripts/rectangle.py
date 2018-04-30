"""Script to play a rectangle stimulus at a given frame rate for a given duration."""

import pyalp as alp


__author__ = "Baptiste Lefebvre"
__copyright__ = "Copyright 2017, Baptiste Lefebvre"
__license__ = "MIT"
__date__ = "2017-08-08"


# Parameters.
x = +0.0  # x-coordinate of the center of the rectangle [um]
y = +0.0  # y-coordinate of the center of the rectangle [um]
w = (16.0 - 1.0) * 60.0  # width of the rectangle [um]
h = (16.0 - 1.0) * 60.0  # height of the rectangle [um]
alpha = 2.3  # pixel size [um]
rate = 40.0  # frame rate [Hz]
duration = 5.0 * 60.0  # duration [s]

# Allocate device.
dev = alp.device.allocate_sequence_bis(verbose=True)

# Define stimulus.
stim = alp.stimulus.Rectangle(x=x, y=y, w=w, h=h, alpha=alpha, rate=rate, duration=duration, verbose=True)

# Display stimulus.
dev.display(stim)
