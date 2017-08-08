import numpy

from .base import Sequence


class Binary(Sequence):
    """Binary sequence."""
    # TODO complete docstring.

    def __init__(self, picture_time):

        bit_planes = 1  # bit depth of the pictures
        pic_num = 2  # number of pictures
        Sequence.__init__(self, bit_planes, pic_num)
        self.picture_time = picture_time

    def get_user_array(self):
        """Get stimulus frames."""

        dtype = numpy.uint8
        width, height = self.device.get_resolution()
        size = width * height
        min_ = numpy.iinfo(dtype).min
        max_ = numpy.iinfo(dtype).max
        dtype = numpy.iinfo(dtype).dtype
        frames = numpy.kron(numpy.array([min_, max_], dtype=dtype), numpy.ones(size, dtype=dtype))

        return frames
