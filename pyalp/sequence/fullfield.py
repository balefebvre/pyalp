import numpy

from .base import Sequence


class FullField(Sequence):
    """Full-field sequence."""
    # TODO complete docstring.

    def __init__(self, footprint_array):

        bit_planes = 8
        pic_num = footprint_array.shape[0]
        Sequence.__init__(self, bit_planes, pic_num)
        self.footprint_array = footprint_array

    def get_user_array(self):
        """Get stimulus frames."""

        dtype = numpy.uint8
        width, height = self.device.get_resolution()
        size = width * height
        frames = numpy.kron(self.footprint_array, numpy.ones(size, dtype=dtype))

        return frames
