import time

import pyalp as alp



class Protocol(object):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self):
        pass


class Checkerboard(Protocol):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, rate, n_repetitions=10):
        Protocol.__init__(self)
        self.rate = rate # Hz
        self.picture_time = int(1.0e6 * self.rate) # ns
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
