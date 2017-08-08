import numpy

from .base import Sequence


class Rectangle(Sequence):
    """Rectangle sequence.

    Parameters
    ----------
    x: float
        x-coordinate of the center of the rectangle [um].
    y: float
        y-coordinate of the center of the rectangle [um].
    w: float
        Width of the rectangle [um].
    h: float
        Height of the rectangle [um].
    alpha: float
        Pixel size [um].
    rate: float
        Frame rate [Hz].

    """

    def __init__(self, x, y, w, h, alpha, rate):

        # Initialize sequence.
        bit_planes = 1  # bit depth of the pictures
        pic_num = 1  # number of pictures
        picture_time = int(1.0e+6 / rate)
        Sequence.__init__(self, bit_planes, pic_num, picture_time=picture_time)

        # Save input parameters.
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.alpha = alpha
        self.rate = rate

    def get_user_array(self):
        """Get stimulus frames."""

        # Allocate frames.
        width, height = self.device.get_resolution()
        shape = (1, height, width)
        dtype = numpy.uint8
        frames = numpy.zeros(shape, dtype=dtype)

        # Define frames.
        i_min = int((self.x - 0.5 * self.w) / self.alpha) + width // 2
        i_max = int((self.x + 0.5 * self.w) / self.alpha) + width // 2 + 1
        j_min = int((self.y - 0.5 * self.h) / self.alpha) + height // 2
        j_max = int((self.y + 0.5 * self.h) / self.alpha) + height // 2 + 1
        frames[:, j_min:j_max, i_min:i_max] = numpy.iinfo(dtype).max

        return frames
