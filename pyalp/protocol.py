import os
import pprint
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
        # TODO check if timing management is correct...
        device.timing(sequence)
        device.put(sequence) # TODO check why in Vialux's example put takes place before timing (no control)
        if __debug__:
            settings = sequence.inquire_settings(device)
            print("White sequence's settings:")
            pprint.pprint(settings)
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
        # TODO check if timing management is correct...
        device.timing(sequence)
        device.put(sequence) # TODO check why in Vialux's example put takes place before timing (no control)
        if __debug__:
            settings = sequence.inquire_settings(device)
            print("Black sequence's settings:")
            pprint.pprint(settings)
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
    def __init__(self, rate=30.0, square_size=20, checkerboard_size=5, nb_repetitions=10, interactive=True):
        Protocol.__init__(self)
        if interactive: # prompt input parameters
            print("# Checkerboard stimulus")
            rate = alp.utils.input("Enter the frame rate [Hz] (e.g. {}): ".format(rate), float)
            square_size = alp.utils.input("Number of pixels to make one side of a single check (e.g. {}): ".format(square_size), int)
            checkerboard_size = alp.utils.input("Number of checks to make one side of the checkerboard (e.g. {}): ".format(checkerboard_size), int)
            nb_repetitions = alp.utils.input("Enter the number of repetitions (e.g. {}): ".format(nb_repetitions), int)
        self.rate = rate # Hz
        self.picture_time = int(1.0e6 / self.rate) # µs
        self.square_size = square_size # px
        self.nb_repetitions = nb_repetitions
        self.checkerboard_size = checkerboard_size * self.square_size # px

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
        device.control_projection(inversion=False, queue_mode=True) # TODO check if queue mode toggle should come after allocations...
        sequence_1 = alp.sequence.Checkerboard(seed=42)
        sequence_2 = alp.sequence.Checkerboard(seed=None)
        # Setup first sequence
        device.allocate(sequence_1)
        # TODO manage control...
        # device.control(sequence_1)
        # TODO manage timing...
        # device.timing(sequence_1)
        # Setup second sequence
        device.allocate(sequence_2)
        # TODO manage control...
        # device.control(sequence_2)
        # TODO manage timing...
        # device.timing(sequence_2)
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
        for rep in range(0, self.nb_repetitions):
            # Wait end of first sequence
            self.wait(device)
            # Manage first sequence
            device.free(sequence_1)
            sequence_1 = alp.sequence.Checkerboard(seed=42)
            device.allocate(sequence_1)
            # TODO manage timing...
            # device.timing(sequence_1)
            device.put(sequence_1)
            device.start(sequence_1)
            # Wait end of second sequence
            self.wait(device)
            # Manage second sequence
            device.free(sequence_2)
            sequence_2 = alp.sequence.Checkerboard(seed=None)
            device.allocate(sequence_2)
            # TODO manage timing...
            # device.timing(sequence_2)
            device.put(sequence_2)
            device.start(sequence_2)
        # Wait end of first sequence
        self.wait(device)
        # Clean first sequence
        device.free(sequence_1)
        # Wait end of second sequence
        device.wait()
        # Clean second sequence
        device.free(sequence_2)
        return


class FullField(Protocol):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, footprint_array, rate=500.0, nb_repetitions=10, infinite_loop=False):
        Protocol.__init__(self)
        self.rate = rate # Hz
        self.picture_time = int(1.0e6 / self.rate) # µs
        self.infinite_loop = infinite_loop
        self.nb_repetitions = nb_repetitions
        self.footprint_array = footprint_array

    def project(self, device):
        device.control_projection(inversion=True)
        sequence = alp.sequence.FullField(self.footprint_array)
        # Set up sequence
        device.allocate(sequence)
        if self.nb_repetitions is not None and not self.infinite_loop:
            device.control_repetitions(sequence, self.nb_repetitions)
        # TODO manage timing...
        device.timing(sequence)
        device.put(sequence) # TODO check why in Vialux's example put takes place before timing (no control)
        # Start sequence
        device.start(sequence, infinite_loop=self.infinite_loop)
        # Wait sequence end
        device.wait(infinite_loop=self.infinite_loop)
        # Clean sequence
        device.free(sequence)
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


class Film(Protocol):
    '''TODO add docstring...
    
    TODO complete...
    '''

    binvec_pathname = os.path.join("E:", "BINVECS") # path to the BINVEC directory

    def __init__(self, user_id=0, bin_id=0, vec_id=0, rate=40.0, nb_lut_frames=200, interactive=True):

        Protocol.__init__(self)

        if interactive:

            print("# Film protocol")

            # Print all the user directories.
            user_dirnames = os.listdir(self.binvec_pathname)
            for user_dirname_id, user_dirname in enumerate(user_dirnames):
                print("  {}. {}".format(user_dirname_id, user_dirname))
            # Prompt user identifier.
            user_id = alp.utils.input("Enter the user number (e.g. {}): ".format(user_id), int)
            user_dirname = user_dirnames[user_id]
            user_pathname = os.path.join(self.binvec_pathname, user_dirname)

            # Print all the BIN files.
            bin_pathname = os.path.join(user_pathname, "Bin")
            bin_filenames = [name for name in os.listdir(bin_pathname) if os.path.isfile(os.path.join(bin_pathname, name))]
            for bin_filename_id, bin_filename in enumerate(bin_filenames):
                print("  {}. {}".format(bin_filename_id, bin_filename))
            # Prompt BIN filename identifier.
            bin_id = alp.utils.input("Enter the .bin file number (e.g. {}): ".format(bin_id), int)
            bin_filename = bin_filenames[bin_id]
            bin_pathname = os.path.join(bin_pathname, bin_filename)

            # Print all the VEC files.
            vec_pathname = os.path.join(user_pathname, "Vec")
            vec_filenames = [name for name in os.listdir(vec_pathname) if os.path.isfile(os.path.join(vec_pathname, name))]
            for vec_filename_id, vec_filename in enumerate(vec_filenames):
                print("  {}. {}".format(vec_filename_id, vec_filename))
            # Prompt VEC filename identifier.
            vec_id = alp.utils.input("Enter the .vec file number (e.g. {}): ".format(vec_id), int)
            vec_filename = vec_filenames[vec_id]
            vec_pathname = os.path.join(vec_pathname, vec_filename)

            # Prompt the frame rate.
            rate = alp.utils.input("Enter the frame rate [Hz] (e.g. {}): ".format(rate), float)

            # Prompt the advanced features.
            advanced = alp.utils.input("Advanced features (y/n): ", lambda arg: arg == "y")

            if advanced:

                # Prompt the number of frames in the look up table.
                nb_lut_frames = alp.utils.input("Number of frames in the look up table (e.g. {}): ".format(nb_lut_frames), int)

        self.user_id = user_id
        self.bin_id = bin_id
        self.vec_id = vec_id

        user_dirnames = os.listdir(self.binvec_pathname)
        user_dirname = user_dirnames[user_id]
        user_pathname = os.path.join(self.binvec_pathname, user_dirname)

        bin_pathname = os.path.join(user_pathname, "Vec")
        bin_filenames = [name for name in os.listdir(bin_pathname) if os.path.isfile(os.path.join(bin_pathname, name))]
        bin_filename = bin_filenames[bin_id]
        self.bin_pathname = os.path.join(bin_pathname, bin_filename)

        vec_pathname = os.path.join(user_pathname, "Bin")
        vec_filenames = [name for name in os.listdir(vec_pathname) if os.path.isfile(os.path.join(vec_pathname, name))]
        vec_filename = vec_filenames[vec_id]
        self.vec_pathname = os.path.join(vec_pathname, vec_filename)

        self.rate = rate

        self.nb_lut_frames = nb_lut_frames

    def get_sequence(self, sequence_id):

        raise NotImplementedError()

    def wait(self, device, sleep_duration=30.0e-3):
        '''TODO add doc...'''
        queue_info = device.inquire_projection('progress')
        while queue_info.nWaitingSequences == 1:
            queue_info = device.inquire_projection('progress')
            time.sleep(sleep_duration)
        device.control_projection(reset_queue=True)

    def project(self, device):
        '''Project film protocol'''
        device.control_projection(inversion=False, queue_mode=True) # TODO check if queue mode toggle should come after allocations...
        sequence_1 = alp.sequence.Checkerboard(seed=42)
        sequence_2 = alp.sequence.Checkerboard(seed=None)
        # Setup first sequence
        device.allocate(sequence_1)
        # TODO manage control...
        # device.control(sequence_1)
        # TODO manage timing...
        # device.timing(sequence_1)
        # Setup second sequence
        device.allocate(sequence_2)
        # TODO manage control...
        # device.control(sequence_2)
        # TODO manage timing...
        # device.timing(sequence_2)
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
        for rep in range(0, self.nb_repetitions):
            # Wait end of first sequence
            self.wait(device)
            # Manage first sequence
            device.free(sequence_1)
            sequence_1 = alp.sequence.Checkerboard(seed=42)
            device.allocate(sequence_1)
            # TODO manage timing...
            # device.timing(sequence_1)
            device.put(sequence_1)
            device.start(sequence_1)
            # Wait end of second sequence
            self.wait(device)
            # Manage second sequence
            device.free(sequence_2)
            sequence_2 = alp.sequence.Checkerboard(seed=None)
            device.allocate(sequence_2)
            # TODO manage timing...
            # device.timing(sequence_2)
            device.put(sequence_2)
            device.start(sequence_2)
        # Wait end of first sequence
        self.wait(device)
        # Clean first sequence
        device.free(sequence_1)
        # Wait end of second sequence
        device.wait()
        # Clean second sequence
        device.free(sequence_2)
        return