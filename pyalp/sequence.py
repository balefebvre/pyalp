import ctypes
import numpy

from pyalp import *
from .base.constant import *



class Sequence(object):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, bit_planes, pic_num):
        # Save input parameters
        self.bit_planes = bit_planes
        self.pic_num = pic_num
        # Save additional parameter
        self.sequence_id = ALP_DEFAULT

    def is_finite(self):
        '''TODO add doc...'''
        return not(self.infinite_loop)


class White(Sequence):
    '''TODO add doc...

    TODO complete...'''
    def __init__(self):
        bit_planes = 1 # bit depth of the pictures
        pic_num = 1 # number of pictures
        Sequence.__init__(self, bit_planes, pic_num)
        self.seq_repeat = 10000 # TODO remove useless parameter...

    def get_user_array(self, device):
        '''Get user array'''
        dtype = 'uint8'
        width, height = device.get_resolution()
        size = width * height
        _, max_, dtype = numpy.iinfo(dtype)
        frame = max_ * numpy.ones(size, dtype=dtype)
        return frame

    def display(self, device):
        '''Display sequence'''
        # Upload and start sequence on device
        sequence_id = device.allocate(self.bit_planes, self.pic_num)
        device.control(sequence_id, seq_repeat=self.seq_repeat)
        device.put(sequence_id, self.get_user_array(device), pic_load=self.pic_num)
        device.timing(sequence_id)
        device.start(sequence_id)
        # Save parameter
        self.sequence_id = sequence_id
        return


class Black(Sequence):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self):
        bit_planes = 1
        pic_num = 1
        Sequence.__init__(self, bit_planes, pic_num)
        self.seq_repeat = 10000 # TODO remove useless parameter...

    def get_user_array(self, device):
        '''Get user array'''
        dtype = 'uint8'
        width, height = device.get_resolution()
        size = width * height
        min_, _, dtype = numpy.iinfo(dtype)
        frame = min_ * numpy.ones(size, dtype=dtype)
        return frame

    def display(self, device):
        '''Display sequence'''
        # Upload and start sequence one device
        sequence_id = device.allocate(self.bit_planes, self.pic_num)
        device.control(sequence_id, seq_repeat=self.seq_repeat)
        device.put(sequence_id, self.get_user_array(device), pic_load=self.pic_num)
        device.timing(sequence_id)
        device.start(sequence_id)
        # Save parameter
        self.sequence_id = sequence_id
        return


class BlackWhite(Sequence):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, infinite_loop=False):
        bit_planes = 1 # bit depth of the pictures
        pic_num = 2 # number of pictures
        Sequence.__init__(self, bit_planes, pic_num)
        self.picture_time = 20000 # µs (i.e. 50 Hz)
        self.infinite_loop = infinite_loop

    def get_user_array(self, device):
        '''Get frames'''
        dtype = 'uint8'
        width, height = device.get_resolution()
        size = width * height
        min_ = numpy.iinfo(dtype).min
        max_ = numpy.iinfo(dtype).max
        dtype = numpy.iinfo(dtype).dtype
        frames = numpy.kron(numpy.array([min_, max_], dtype=dtype), numpy.ones(size, dtype=dtype))
        return frames

    def display(self, device):
        '''Display sequence'''
        sequence_id = device.allocate(self.bit_planes, self.pic_num)
        device.put(sequence_id, self.get_user_array(device), pic_load=self.pic_num)
        device.timing(sequence_id, picture_time=self.picture_time)
        device.start(sequence_id, infinite_loop=self.infinite_loop)
        # Save parameter
        self.sequence_id = sequence_id
        return


class FullField(Sequence):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, footprint_array):
        bit_planes = 8
        pic_num = footprint_array.shape[0]
        Sequence.__init__(self, bit_planes, pic_num)
        self.footprint_array = footprint_array
        self.seq_repeat = 1 # TODO remove useless parameter...

    def get_user_array(self, device):
        dtype = 'uint8'
        width, height = device.get_resolution()
        size = width * height
        frames = numpy.kron(footprint_array, numpy.ones(size, dtype='uint8'))
        return frames

    def display(self, device):
        # Upload and start sequence one device
        sequence_id = device.allocate(self.bit_planes, self.pic_num)
        device.control(sequence_id, seq_repeat=self.seq_repeat)
        device.put(sequence_id, self.get_user_array(device), pic_load=self.pic_num)
        device.timing(sequence_id)
        device.start(sequence_id)
        # Save parameter
        self.sequence_id = sequence_id
        return


class Sequence(object):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, bit_planes=None, pic_num=None,
                 illuminate_time=ALP_DEFAULT, picture_time=ALP_DEFAULT,
                 synch_delay=ALP_DEFAULT, synch_pulse_width=ALP_DEFAULT,
                 trigger_in_delay=ALP_DEFAULT, infinite_loop=False,
                 pic_offset=ALP_DEFAULT, pic_load=ALP_DEFAULT):
        assert bit_planes is not None, "Invalid bit_planes value: {}".format(bit_planes)
        self.bit_planes = bit_planes
        assert pic_num is not None, "Invalid pic_num values: {}".format(pic_num)
        self.pic_num = pic_num
        self.illuminate_time = illuminate_time
        self.picture_time = picture_time
        self.synch_delay = synch_delay
        self.synch_pulse_width = synch_pulse_width
        self.trigger_in_delay = trigger_in_delay
        self.infinite_loop = infinite_loop
        self.pic_offset = pic_offset # TODO check if it should be defined somewhere else...
        self.pic_load = pic_load # TODO check if it should be defined somewhere else...

class Checkerboard(Sequence):
    '''TODO add doc...

    TODO complete...
    '''
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
        Sequence.__init__(bit_planes=8, pic_num=300, picture_time=int(1.0e6 / self.rate))
        # TODO remove following lines...
        # self.picture_time = int(1.0e6 / self.rate) # ns
        # self.synch_delay = ALP_DEFAULT
        # self.synch_pulse_width = ALP_DEFAULT
        # self.trigger_in_delay = ALP_DEFAULT
        # self.infinite_loop = False
        # self.pic_offset = ALP_DEFAULT
        # self.pic_load = ALP_DEFAULT

    def get_user_array(self, device):
        '''TODO add doc...'''
        # Allocate frame
        width, height = device.get_resolution()
        shape = (width, height, self.pic_num)
        frames = numpy.zeros(shape, dtype='uint8')
        # Generate data
        shape = (self.n_checks, self.n_checks, self.pic_num)
        numpy.random.seed(self.seed)
        data = numpy.random.randint(0, high=2, shape=shape, dtype='uint8')
        # Scale data
        _, max_, _ = numpy.iinfo('uint8')
        data = max_ * data
        # Define frames
        x_min = (self.width - self.checkerboard_size) // 2
        x_max = x_min + self.width
        y_min = (self.height - self.checkerboard_size) // 2
        y_max = y_min + self.height
        frames[x_min:x_max, y_min:y_max, :] = numpy.kron(data, numpy.ones((self.check_size, self.check_size, 1)))
        # Return frames
        return frames

    def display(self, device):
        device.invert_projection()
        sequence_id = device.allocate(self.bit_planes, self.pic_num)
        device.timing(sequence_id, picture_time=self.picture_time)
        raise NotImplementedError()
