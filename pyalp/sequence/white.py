import numpy

from .base import Sequence


class White(Sequence):
    """White sequence."""
    # TODO complete docstring.

    def __init__(self):

        bit_planes = 1  # bit depth of the pictures
        pic_num = 1  # number of pictures
        Sequence.__init__(self, bit_planes, pic_num)

    def get_user_array(self):
        """Get user array"""

        dtype = numpy.uint8
        width, height = self.device.get_resolution()
        size = width * height
        max_ = numpy.iinfo(dtype).max
        dtype = numpy.iinfo(dtype).dtype
        frame = max_ * numpy.ones(size, dtype=dtype)

        return frame
