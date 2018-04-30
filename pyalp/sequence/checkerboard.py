import numpy

from .base import Sequence


class Checkerboard(Sequence):
    """TODO add doc...

    TODO complete...
    """
    def __init__(self, check_size=30, n_checks=10, rate=50.0, n_repetitions=None, seed=None):
        # Save input parameters
        self.check_size = check_size  # px
        self.n_checks = n_checks
        self.rate = rate  # Hz
        self.n_repetitions = n_repetitions
        self.seed = seed
        # Save computed parameters
        self.id = None  # identifier set by device during sequence allocation
        self.checkerboard_size = self.n_checks * self.check_size  # px
        # TODO assert(isinstance(n_repetitions, int))
        # TODO assert(0 <= sequence.n_repetitions and sequence.n_repetitions <= 1048576)
        bit_planes = 8  # bit depth of the pictures
        pic_num = 50  # number of pictures
        Sequence.__init__(self, bit_planes, pic_num)
        # TODO remove following lines...
        # self.picture_time = int(1.0e6 / self.rate) # ns
        # self.synch_delay = ALP_DEFAULT
        # self.synch_pulse_width = ALP_DEFAULT
        # self.trigger_in_delay = ALP_DEFAULT
        # self.infinite_loop = False
        # self.pic_offset = ALP_DEFAULT
        # self.pic_load = ALP_DEFAULT

    def get_user_array(self):
        """TODO add doc..."""
        # Allocate frame
        width, height = self.device.get_resolution()
        shape = (width, height, self.pic_num)
        dtype = 'uint8'
        frames = numpy.zeros(shape, dtype=dtype)
        # Generate data
        size = (self.n_checks, self.n_checks, self.pic_num)
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
        frames[x_min:x_max, y_min:y_max, :] = numpy.kron(data, numpy.ones((self.check_size, self.check_size, 1)))
        # Transpose frames
        frames = numpy.transpose(frames)
        # TODO remove the following lines.
        # print("frames: {}".format(frames))
        print("frames.shape: {}".format(frames.shape))
        print("numpy.amin(frames): {}".format(numpy.amin(frames)))
        print("numpy.amax(frames): {}".format(numpy.amax(frames)))
        import matplotlib.pyplot as plt
        import os
        plt.imshow(frames[:, :, 0])
        plt.savefig(os.path.expanduser(os.path.join("~", "checkerboard.svg")))
        # Return frames
        return frames

    def display(self):
        self.device.invert_projection()
        sequence_id = self.device.allocate_sequence_bis(self.bit_planes, self.pic_num)
        self.device.timing(sequence_id, picture_time=self.picture_time)
        raise NotImplementedError()
