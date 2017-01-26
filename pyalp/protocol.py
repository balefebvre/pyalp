import time

import pyalp as alp



class Protocol(object):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self):
        pass


class White(Protocol):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, rate=50.0, nb_repetitions=None, infinite_loop=False):
        Protocol.__init__(self)
        self.rate = rate # Hz (frame rate)
        self.picture_time = int(1.0e6 / self.rate) # µs (time between the start of two consecutive pictures)
        self.nb_repetitions = nb_repetitions
        self.infinite_loop = infinite_loop

    def project(self, device):
        device.control_projection(inversion=True)
        sequence = alp.sequence.White()
        # Set up sequence
        device.allocate(sequence)
        if self.nb_repetitions is not None and not self.infinite_loop:
            device.control_repetitions(sequence, self.nb_repetitions)
        # TODO manage timing
        # device.timing(sequence)
        device.put(sequence) # TODO check why in Vialux's example put takes place before timing (no control)
        # Start sequence
        device.start(sequence, infinite_loop=self.infinite_loop)
        # Wait sequence end
        device.wait(infinite_loop=self.infinite_loop)
        # Clean sequence
        device.free(sequence)
        return


class Black(Protocol):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, rate=50.0, nb_repetitions=None, infinite_loop=False):
        Protocol.__init__(self)
        self.rate = rate # Hz (frame rate)
        self.picture_time = int(1.0e6 / self.rate) # µs (time between the start of two consecutive pictures)
        self.nb_repetitions = nb_repetitions
        self.infinite_loop = infinite_loop

    def project(self, device):
        device.control_projection(inversion=True)
        sequence = alp.sequence.Black()
        # Set up sequence
        device.allocate(sequence)
        if self.nb_repetitions is not None and not self.infinite_loop:
            device.control_repetitions(sequence, self.nb_repetitions)
        # TODO manage timing...
        # device.timing(sequence)
        device.put(sequence) # TODO check why in Vialux's example put takes place before timing (no control)
        # Start sequence
        device.start(sequence, infinite_loop=self.infinite_loop)
        # Wait sequence end
        device.wait(infinite_loop=self.infinite_loop)
        # Clean sequence
        device.free(sequence)
        return


class BlackWhite(Protocol):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, rate=50.0, nb_repetitions=None, infinite_loop=False):
        Protocol.__init__(self)
        self.rate = rate # Hz (frame rate)
        self.picture_time = int(1.0e6 / self.rate) # µs (time between the start of two consecutive pictures)
        self.nb_repetitions = nb_repetitions
        self.infinite_loop = infinite_loop

    def project(self, device):
        device.control_projection(inversion=True)
        sequence = alp.sequence.BlackWhite()
        # Set up sequence
        device.allocate(sequence)
        if self.nb_repetitions is not None and not self.infinite_loop:
            device.control_repetitions(sequence, self.nb_repetitions)
        # TODO manage timing...
        # device.timing(sequence)
        device.put(sequence) # TODO check why in Vialux's example put takes place before timing (no control)
        # Start sequence
        device.start(sequence, infinite_loop=self.infinite_loop)
        # Wait sequence end
        device.wait(infinite_loop=self.infinite_loop)
        # Clean sequence
        device.free(sequence)
        return


class Checkerboard(Protocol):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, rate, n_repetitions=10):
        Protocol.__init__(self)
        self.rate = rate # Hz
        self.picture_time = int(1.0e6 * self.rate) # µs
        self.n_repetitions = n_repetitions
        self.square_size = 30 # px
        self.checkerboard_size = 5 * self.square_size # px

    def wait(self, device, sleep_duration=30.0e-3):
        '''TODO add doc...'''
        queue_info = device.inquire_projection('progress')
        while queue_info.nWaitingSequences == 1:
            queue_info = device.inquire_projection('progress')
            time.sleep(sleep_duration)
        device.control_projection(reset_queue=True)
        return

    def project(self, device):
        '''Project checkerboard protocol'''
        device.control_projection(inversion=True, queue_mode=True) # TODO check if queue mode toggle should come after allocations...
        sequence_1 = alp.sequence.Checkerboard(seed=42)
        sequence_2 = alp.sequence.Checkerboard(seed=None)
        # Setup first sequence
        device.allocate(sequence_1)
        device.control(sequence_1)
        device.timing(sequence_1)
        # Setup second sequence
        device.allocate(sequence_2)
        device.control(sequence_2)
        device.timing(sequence_2)
        # Start first sequence
        print("Start sequence 1")
        device.put(sequence_1)
        device.start(sequence_1)
        # Start second sequence
        print("Start sequence 2")
        device.put(sequence_2)
        device.start(sequence_2)
        # For each repetition
        print("Start infernal loop")
        for rep in range(0, self.n_repetitions):
            # Wait end of first sequence
            self.wait(device)
            # Manage first sequence
            device.free(sequence_1)
            sequence_1 = alp.sequence.Checkerboard(seed=42)
            device.allocate(sequence_1)
            device.timing(sequence_1)
            device.put(sequence_1)
            device.start(sequence_1)
            # Wait end of second sequence
            self.wait(device)
            # Manage second sequence
            device.wait(sequence_2)
            device.free(sequence_2)
            sequence_2 = alp.sequence.Checkerboard(seed=None)
            device.allocate(sequence_2)
            device.timing(sequence_2)
            device.put(sequence_2)
            device.start(sequence_2)
        # Wait end of first sequence
        self.wait(device)
        # Clean first sequence
        device.free(sequence_1)
        # Wait end of second sequence
        self.wait(device)
        # Clean second sequence
        device.free(sequence_2)
        return


class MovingBar(Protocol):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, w, l, x, y, theta, v, rate, n_repetitions=10):
        Protocol.__init__(self)
        self.w = w # arb. unit (i.e. width)
        self.l = l # arb. unit (i.e. length)
        self.x = x # arb. unit (i.e. x-coordinate)
        self.y = y # arb. unit (i.e. y-coordinate)
        self.theta = theta # rad (i.e. direction & orientation)
        self.v = v # arb.unit / s (i.e. velocity)
        self.rate = rate # Hz
        self.picture_time = int(1.0e6 * self.rate) # ns
        self.n_repetitions = n_repetitions
        self.square_size = 30 # px
        self.checkerboard_size = 5 * self.square_size # px

    def project(self, device):
        '''Project moving bar protocol'''
        return
