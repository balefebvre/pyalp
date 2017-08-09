import numpy

from .base import Sequence


class CheckerboardBis(Sequence):
    """Checkerboard sequence

    Parameters
    ----------
    sequence_id: integer
    check_size: integer
    nb_checks: integer
    nb_frames: integer

    """
    # TODO complete docstring.

    def __init__(self, sequence_id, check_size, nb_checks, nb_frames, rate):

        bit_planes = 1
        pic_num = nb_frames
        picture_time = int(1.0e+6 / rate)

        Sequence.__init__(self, bit_planes, pic_num, picture_time=picture_time)

        self.sequence_id = sequence_id
        self.check_size = check_size
        self.nb_checks = nb_checks
        self.nb_frames = nb_frames

        self.seed = self.sequence_id
        self.checkerboard_size = self.check_size * self.nb_checks

    def get_user_array(self):
        """TODO add docstring"""

        # Allocate frame
        width, height = self.device.get_resolution()
        shape = (self.nb_frames, height, width)
        dtype = numpy.uint8
        frames = numpy.zeros(shape, dtype=dtype)
        # Generate data
        size = (self.nb_frames, self.nb_checks, self.nb_checks)
        numpy.random.seed(self.seed)
        data = numpy.random.randint(0, high=2, size=size, dtype=dtype)
        # Scale data
        max_ = numpy.iinfo(dtype).max
        data = max_ * data
        # Define frames
        x_min = (width - self.checkerboard_size) // 2
        x_max = x_min + self.checkerboard_size
        y_min = (height - self.checkerboard_size) // 2
        y_max = y_min + self.checkerboard_size
        data = numpy.kron(data, numpy.ones((1, self.check_size, self.check_size)))
        frames[:, y_min:y_max, x_min:x_max] = data
        # TODO check if the following two lines are necessary.
        # # Transpose frames
        # frames = numpy.transpose(frames)

        return frames
