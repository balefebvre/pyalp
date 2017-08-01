# import ctypes
from ctypes import c_ulong, byref
import numpy

from pyalp import *
from .base.constant import *


class Sequence(object):
    """TODO add doc...

    TODO complete...
    """
    def __init__(self, bit_planes, pic_num, pic_offset=ALP_DEFAULT, pic_load=ALP_DEFAULT):
        # Save input parameters
        self.bit_planes = bit_planes
        self.pic_num = pic_num
        self.pic_offset = pic_offset
        self.pic_load = pic_load
        self.illuminate_time = ALP_DEFAULT
        self.picture_time = int(1.0e6 / 50.0)
        self.synch_delay = ALP_DEFAULT
        self.synch_pulse_width = ALP_DEFAULT
        self.trigger_in_delay = ALP_DEFAULT
        # Save additional parameter
        self.sequence_id = ALP_DEFAULT
        self.device = None

    def is_finite(self):
        """TODO add doc..."""

        return not(self.infinite_loop)

    def inquire(self, device, inquire_type):
        """Inquire a parameter setting on the picture sequence"""
        DeviceId = c_ulong(device.id)
        SequenceId = c_ulong(self.id)
        InquireType = c_ulong(inquire_type)
        UserVar = c_ulong(ALP_DEFAULT)
        UserVarPtr = byref(UserVar)
        ret_val = api.AlpSeqInquire(DeviceId, SequenceId, InquireType, UserVarPtr)
        if ret_val == ALP_OK:
            ret_val = UserVar.value
            return ret_val
        else:
            raise Exception("AlpSeqInquire: {}".format(ret_val))

    def inquire_bit_planes(self, device):
        """Inquire the bit depth of the pictures in the sequence"""
        self.bit_planes = self.inquire(device, ALP_BITPLANES)
        return self.bit_planes

    def inquire_bit_num(self, device):
        """Inquire the bit depth for display"""
        self.bit_num = self.inquire(device, ALP_BITNUM)
        return self.bit_num

    def inquire_bin_mode(self, device):
        """Inquire the status of the binary mode for display"""
        self.bin_mode = self.inquire(device, ALP_BIN_MODE)
        return self.bin_mode

    def inquire_pic_num(self, device):
        """Inquire the number of pictures in the equence"""
        self.pic_num = self.inquire(device, ALP_PICNUM)
        return self.pic_num

    def inquire_first_frame(self, device):
        """Inquire the number of the first picture in the sequence selected for display"""
        self.first_frame = self.inquire(device, ALP_FIRSTFRAME)
        return self.first_frame

    def inquire_last_frame(self, device):
        """Inquire the number of the last picture in the sequence selected for display"""
        self.last_frame = self.inquire(device, ALP_LASTFRAME)
        return self.last_frame

    # TODO add inquiry for ALP_SCROLL_FROM_ROW, ALP_SCROLL_TO_ROW,
    # ALP_FIRSTLINE, ALP_LASTLINE, ALP_LINE_INC

    def inquire_sequence_repeat(self, device):
        """Inquire the number of automatically repeated displays of the sequence"""
        self.sequence_repeat = self.inquire(device, ALP_SEQ_REPEAT)
        return self.sequence_repeat

    def inquire_picture_time(self, device):
        """Inquire the time between the start of consecutive pictures"""
        self.picture_time = self.inquire(device, ALP_PICTURE_TIME)
        return self.picture_time

    def inquire_min_picture_time(self, device):
        """Inquire the minimum time between the start of consecutive pictures"""
        self.min_picture_time = self.inquire(device, ALP_MIN_PICTURE_TIME)
        return self.min_picture_time

    def inquire_max_picture_time(self, device):
        """Inquire the maximum time between the start of consecutive pictures"""
        self.max_picture_time = self.inquire(device, ALP_MAX_PICTURE_TIME)
        return self.max_picture_time

    def inquire_illuminate_time(self, device):
        """Inquire the duration of the display of one picture"""
        self.illuminate_time = self.inquire(device, ALP_ILLUMINATE_TIME)
        return self.illuminate_time

    def inquire_min_illuminate_time(self, device):
        """Inquire the minimum duration of the display of one picture"""
        self.min_illuminate_time = self.inquire(device, ALP_MIN_ILLUMINATE_TIME)
        return self.min_illuminate_time

    def inquire_on_time(self, device):
        """Inquire the total active projection time"""
        self.on_time = self.inquire(device, ALP_ON_TIME)
        return self.on_time

    def inquire_off_time(self, device):
        """Inquire the total inactive projection time"""
        self.off_time = self.inquire(device, ALP_OFF_TIME)
        return self.off_time

    # TODO add inquiry for ALP_SYNCH_DELAY, ALP_MAX_SYNCH_DELAY,
    # ALP_SYNCH_PULSEWIDTH, ALP_TRIGGER_IN_DELAY, ALP_MAX_TRIGGER_IN_DELAY

    def inquire_data_format(self, device):
        """Inquire the active image data format"""
        self.data_format = self.inquire(device, ALP_DATA_FORMAT)
        return self.data_format

    def inquire_sequence_put_lock(self, device):
        """Inquire the status of the lock protecting sequence data against
        writing during display"""
        self.sequence_put_lock = self.inquire(device, ALP_SEQ_PUT_LOCK)
        return self.sequence_put_lock

    # TODO add inquiry for ALP_FLUT_MODE, ALP_FLUT_ENTRIES9, ALP_FLUT_OFFSET9

    # TODO add inquiry for ALP_PWM_MODE

    def inquire_settings(self, device):
        settings = {
            'bit planes': self.inquire_bit_planes(device),
            'bit num': self.inquire_bit_num(device),
            'bin mode': self.inquire_bin_mode(device),
            'pic num': self.inquire_pic_num(device),
            'first frame': self.inquire_first_frame(device),
            'last frame': self.inquire_last_frame(device),
            # TODO complete...
            'sequence repeat': self.inquire_sequence_repeat(device),
            'picture time': self.inquire_picture_time(device),
            'min picture time': self.inquire_min_picture_time(device),
            'max picture time': self.inquire_max_picture_time(device),
            'illuminate time': self.inquire_illuminate_time(device),
            'min illuminate time': self.inquire_min_illuminate_time(device),
            'on time': self.inquire_on_time(device),
            'off time': self.inquire_off_time(device),
            # TODO complete...
            'data format': self.inquire_data_format(device),
            # 'sequence put lock': self.inquire_sequence_put_lock(device),
            # TODO complete...
        }
        return settings

    def control(self, control_type, control_value):
        """TODO add docstring."""

        self.device.control(self, control_type, control_value)

        return

    def control_nb_repetitions(self, nb_repetitions):
        """TODO add docstring."""

        self.control(ALP_SEQ_REPEAT, nb_repetitions)

        return

    def control_bit_number(self, bit_number):
        """TODO add docstring."""

        self.control(ALP_BITNUM, bit_number)

        return

    def control_binary_mode(self, binary_mode):
        """TODO add docstring."""

        if binary_mode is 'normal':
            self.control(ALP_BIN_MODE, ALP_BIN_NORMAL)
        elif binary_mode is 'uninterrupted':
            self.control(ALP_BIN_MODE, ALP_BIN_UNINTERRUPTED)
        else:
            raise NotImplementedError()

        return


class White(Sequence):
    """TODO add doc...

    TODO complete..."""
    def __init__(self):
        bit_planes = 1 # bit depth of the pictures
        pic_num = 1 # number of pictures
        Sequence.__init__(self, bit_planes, pic_num)

    def get_user_array(self, device):
        """Get user array"""
        dtype = 'uint8'
        width, height = device.get_resolution()
        size = width * height
        max_ = numpy.iinfo(dtype).max
        dtype = numpy.iinfo(dtype).dtype
        frame = max_ * numpy.ones(size, dtype=dtype)
        return frame


class Black(Sequence):
    """TODO add doc...

    TODO complete...
    """
    def __init__(self):
        bit_planes = 1 # bit depth of the pictures
        pic_num = 1 # number of pictures
        Sequence.__init__(self, bit_planes, pic_num)

    def get_user_array(self, device):
        """Get user array"""
        dtype = 'uint8'
        width, height = device.get_resolution()
        size = width * height
        min_ = numpy.iinfo(dtype).min
        dtype = numpy.iinfo(dtype).dtype
        frame = min_ * numpy.ones(size, dtype=dtype)
        return frame


class BlackWhite(Sequence):
    """TODO add doc...

    TODO complete...
    """
    def __init__(self, infinite_loop=False):
        bit_planes = 1 # bit depth of the pictures
        pic_num = 2 # number of pictures
        Sequence.__init__(self, bit_planes, pic_num)

    def get_user_array(self, device):
        """Get frames"""
        dtype = 'uint8'
        width, height = device.get_resolution()
        size = width * height
        min_ = numpy.iinfo(dtype).min
        max_ = numpy.iinfo(dtype).max
        dtype = numpy.iinfo(dtype).dtype
        frames = numpy.kron(numpy.array([min_, max_], dtype=dtype), numpy.ones(size, dtype=dtype))
        return frames


class Binary(Sequence):
    """TODO add docstring.

    TODO complete.

    """

    def __init__(self, picture_time):
        bit_planes = 1  # bit depth of the pictures
        pic_num = 2  # number of pictures
        Sequence.__init__(self, bit_planes, pic_num)
        self.picture_time = picture_time

    def get_user_array(self, device):
        """TODO add docstring."""
        dtype = 'uint8'
        width, height = device.get_resolution()
        size = width * height
        min_ = numpy.iinfo(dtype).min
        max_ = numpy.iinfo(dtype).max
        dtype = numpy.iinfo(dtype).dtype
        frames = numpy.kron(numpy.array([min_, max_], dtype=dtype), numpy.ones(size, dtype=dtype))
        return frames


class FullField(Sequence):
    """TODO add doc...

    TODO complete...
    """
    def __init__(self, footprint_array):
        bit_planes = 8
        pic_num = footprint_array.shape[0]
        Sequence.__init__(self, bit_planes, pic_num)
        self.footprint_array = footprint_array

    def get_user_array(self, device):
        dtype = 'uint8'
        width, height = device.get_resolution()
        size = width * height
        frames = numpy.kron(self.footprint_array, numpy.ones(size, dtype='uint8'))
        return frames


# TODO delete...
# class Sequence(object):
#     """TODO add doc...
#
#     TODO complete...
#     """
#     def __init__(self, bit_planes=None, pic_num=None,
#                  illuminate_time=ALP_DEFAULT, picture_time=ALP_DEFAULT,
#                  synch_delay=ALP_DEFAULT, synch_pulse_width=ALP_DEFAULT,
#                  trigger_in_delay=ALP_DEFAULT, infinite_loop=False,
#                  pic_offset=ALP_DEFAULT, pic_load=ALP_DEFAULT):
#         assert bit_planes is not None, "Invalid bit_planes value: {}".format(bit_planes)
#         self.bit_planes = bit_planes
#         assert pic_num is not None, "Invalid pic_num values: {}".format(pic_num)
#         self.pic_num = pic_num
#         self.illuminate_time = illuminate_time
#         self.picture_time = picture_time
#         self.synch_delay = synch_delay
#         self.synch_pulse_width = synch_pulse_width
#         self.trigger_in_delay = trigger_in_delay
#         self.infinite_loop = infinite_loop
#         self.pic_offset = pic_offset # TODO check if it should be defined somewhere else...
#         self.pic_load = pic_load # TODO check if it should be defined somewhere else...

class Checkerboard(Sequence):
    """TODO add doc...

    TODO complete...
    """
    def __init__(self, check_size=30, n_checks=10, rate=50.0, n_repetitions=None, seed=None):
        # Save input parameters
        self.check_size = check_size # px
        self.n_checks = n_checks
        self.rate = rate # Hz
        self.n_repetitions = n_repetitions
        self.seed = seed
        # Save computed parameters
        self.id = None # identifier set by device during sequence allocation
        self.checkerboard_size = self.n_checks * self.check_size # px
        # TODO assert(isinstance(n_repetitions, int))
        # TODO assert(0 <= sequence.n_repetitions and sequence.n_repetitions <= 1048576)
        bit_planes = 8 # bit depth of the pictures
        pic_num = 50 # number of pictures
        Sequence.__init__(self, bit_planes, pic_num)
        # TODO remove following lines...
        # self.picture_time = int(1.0e6 / self.rate) # ns
        # self.synch_delay = ALP_DEFAULT
        # self.synch_pulse_width = ALP_DEFAULT
        # self.trigger_in_delay = ALP_DEFAULT
        # self.infinite_loop = False
        # self.pic_offset = ALP_DEFAULT
        # self.pic_load = ALP_DEFAULT

    def get_user_array(self, device):
        """TODO add doc..."""
        # Allocate frame
        width, height = device.get_resolution()
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

    def display(self, device):
        device.invert_projection()
        sequence_id = device.allocate(self.bit_planes, self.pic_num)
        device.timing(sequence_id, picture_time=self.picture_time)
        raise NotImplementedError()
