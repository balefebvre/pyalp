import gc
import os

import pyalp.io
import pyalp.sequence
import pyalp.utils

from .base import Stimulus


class Film(Stimulus):
    """Film stimulus

    Parameters
    ----------
    bin_pathname: none | string, optional
        Path name to the .bin file.
    vec_pathname: none | string, optional
        Path name to the .vec file.
    rate: float, optional
        Frame rate [Hz]. The default value is 30.0.
    sequence_size: integer, optional
        Number of frames each sequence. The default value is 200.
    interactive: boolean, optional
        Specify if it should prompt the input parameters. The default value is False.
    verbose: boolean, optional
        Verbose mode. The default value is False.

    """

    dirname = os.path.join("E:", "BINVECS")
    # dirname = os.path.expanduser(os.path.join("~", ".pyalp", "films"))  # TODO remove.

    def __init__(self, bin_pathname=None, vec_pathname=None, rate=30.0, sequence_size=200,
                 interactive=False, verbose=False):

        Stimulus.__init__(self)

        self.bin_pathname = bin_pathname
        self.vec_pathname = vec_pathname
        self.rate = rate
        self.sequence_size = sequence_size

        if interactive:

            self.prompt_input_arguments()

        # Read .vec file.
        self.frame_ids = pyalp.io.load_vec(self.vec_pathname)
        self.nb_frames = len(self.frame_ids)
        self.nb_sequences = int(self.nb_frames / self.sequence_size)
        self.nb_cycles = int(self.nb_sequences / 2)

        # Read header of .bin file.
        self.bin_header = pyalp.io.load_bin_header(self.bin_pathname)

        if verbose:

            self.print_settings()

    def prompt_input_arguments(self, sep=""):
        """Prompt the input arguments.

        Parameter
        ---------
        sep: string, optional
            Prompt separator. The default value is \"\"

        """

        print(sep)

        # Print all the user directories.
        user_dirnames = os.listdir(self.dirname)
        for user_dirname_id, user_dirname in enumerate(user_dirnames):
            print("  {}. {}".format(user_dirname_id, user_dirname))
        # Prompt user identifier.
        prompt = "Enter the user number (e.g. 0): "
        user_id = pyalp.utils.input(prompt, int)
        user_dirname = user_dirnames[user_id]
        user_pathname = os.path.join(self.dirname, user_dirname)

        print(sep)

        # Print all the .bin files.
        bin_pathname = os.path.join(user_pathname, "Bin")
        bin_filenames = [name for name in os.listdir(bin_pathname) if os.path.isfile(os.path.join(bin_pathname, name))]
        for bin_filename_id, bin_filename in enumerate(bin_filenames):
            print("  {}. {}".format(bin_filename_id, bin_filename))
        # Prompt .bin filename identifier.
        prompt = "Enter the .bin file number (e.g. 0): "
        bin_id = pyalp.utils.input(prompt, int)
        bin_filename = bin_filenames[bin_id]
        self.bin_pathname = os.path.join(bin_pathname, bin_filename)

        print(sep)

        # Print all the .vec files.
        vec_pathname = os.path.join(user_pathname, "Vec")
        vec_filenames = [name for name in os.listdir(vec_pathname) if os.path.isfile(os.path.join(vec_pathname, name))]
        for vec_filename_id, vec_filename in enumerate(vec_filenames):
            print("  {}. {}".format(vec_filename_id, vec_filename))
        # Prompt .vec filename identifier.
        prompt = "Enter the .vec file number (e.g. 0): "
        vec_id = pyalp.utils.input(prompt, int)
        vec_filename = vec_filenames[vec_id]
        self.vec_pathname = os.path.join(vec_pathname, vec_filename)

        print(sep)

        # Prompt the frame rate.
        prompt = "Enter the frame rate [Hz] (e.g. {}): ".format(self.rate)
        self.rate = pyalp.utils.input(prompt, float)

        print(sep)

        # Prompt the advanced features.
        prompt = "Advanced features (y/n): "
        advanced = pyalp.utils.input(prompt, lambda arg: arg == "y")

        if advanced:
            # Prompt the number of frames in each sequence.
            prompt = "Number of frames in each sequence (e.g. {}): ".format(self.sequence_size)
            self.sequence_size = pyalp.utils.input(prompt, int)

        print(sep)

        return

    def print_settings(self):
        """Print settings."""

        print("----------------- Film stimulus ------------------")
        print(".bin pathname: {}".format(self.bin_pathname))
        print(".vec pathname: {}".format(self.vec_pathname))
        print("frame rate: {} Hz".format(self.rate))
        print("sequence size: {}".format(self.sequence_size))
        print("number of frames: {}".format(self.nb_frames))
        print("number of sequences: {}".format(self.nb_sequences))
        print("number of cycles: {}".format(self.nb_cycles))
        print(".bin header: {}".format(self.bin_header))
        print("--------------------------------------------------")
        print("")

        return

    def display(self, device):
        """Display stimulus.

        Parameter
        ---------
        device: Device
            ALP device.

        """

        sequence_1 = None
        sequence_2 = None

        if self.nb_frames > 0 * self.sequence_size:  # i.e. enough frames

            # 1. Allocate 1st sequence of frames.
            # Define 1st sequence of frames.
            sequence_id_1 = 0
            nb_frames = min(self.sequence_size, self.nb_frames - 0 * self.sequence_size)
            sequence_1 = pyalp.sequence.Film(sequence_id_1, self.bin_pathname, self.frame_ids, nb_frames,
                                             self.sequence_size, self.rate)
            # Allocate memory for 1st sequence of frames.
            device.allocate(sequence_1)
            # Control the timing properties of 1st sequence display.
            sequence_1.control_timing()

        if self.nb_frames > 1 * self.sequence_size:  # i.e. enough frames

            # 2. Allocate 2nd sequence of frames.
            # Define 2nd sequence of frames.
            sequence_id_2 = 1
            nb_frames = min(self.sequence_size, self.nb_frames - 1 * self.sequence_size)
            sequence_2 = pyalp.sequence.Film(sequence_id_2, self.bin_pathname, self.frame_ids, nb_frames,
                                             self.sequence_size, self.rate)
            # Allocate memory for 2nd sequence of frames.
            device.allocate(sequence_2)
            # Control the timing properties of 2nd sequence display.
            sequence_2.control_timing()

        # 3. Play on DMD.
        # Set up queue mode.
        device.control_projection(queue_mode=True)
        # Transmit and start 1st sequence of frames into memory.
        if self.nb_frames > 0 * self.sequence_size:  # i.e. enough frames
            sequence_1.load()
            sequence_1.start()
        # Transmit and start 2nd sequence of frames into memory.
        if self.nb_frames > 1 * self.sequence_size:  # i.e. enough frames
            sequence_2.load()
            sequence_2.start()
        # Force garbage collection.
        gc.collect()

        # 4. Repeat.
        for cycle_id in range(1, self.nb_cycles):

            # a. Wait completion of 1st sequence.
            device.synchronize()
            # b. Free 1st sequence.
            sequence_1.free()
            # c. Reallocate 1st sequence.
            sequence_id_1 = 2 * cycle_id + 0
            nb_frames = self.sequence_size
            sequence_1 = pyalp.sequence.Film(sequence_id_1, self.bin_pathname, self.frame_ids, nb_frames,
                                             self.sequence_size, self.rate)
            device.allocate(sequence_1)
            sequence_1.control_timing()
            sequence_1.load()
            sequence_1.start()
            gc.collect()
            # d. Wait completion of 2nd sequence.
            device.synchronize()
            # e. Free 2nd sequence.
            sequence_2.free()
            # f. Reallocate 2nd sequence.
            sequence_id_2 = 2 * cycle_id + 1
            nb_frames = self.sequence_size
            sequence_2 = pyalp.sequence.Film(sequence_id_2, self.bin_pathname, self.frame_ids, nb_frames,
                                             self.sequence_size, self.rate)
            device.allocate(sequence_2)
            sequence_2.control_timing()
            sequence_2.load()
            sequence_2.start()
            gc.collect()

        if self.nb_cycles > 0 and self.nb_frames > (self.nb_cycles * 2 + 0) * self.sequence_size:
            # i.e. remaining frames

            # a. Wait completion of 1st sequence.
            device.synchronize()
            # b. Free 1st sequence.
            sequence_1.free()
            # c. Reallocate 1st sequence.
            sequence_id_1 = 2 * self.nb_cycles + 0
            nb_frames = min(self.sequence_size, self.nb_frames - sequence_id_1 * self.sequence_size)
            sequence_1 = pyalp.sequence.Film(sequence_id_1, self.bin_pathname, self.frame_ids, nb_frames,
                                             self.sequence_size, self.rate)
            device.allocate(sequence_1)
            sequence_1.control_timing()
            sequence_1.load()
            sequence_1.start()
            gc.collect()

        if self.nb_cycles > 0 and self.nb_frames > (self.nb_cycles * 2 + 1) * self.sequence_size:
            # i.e. remaining frames

            # a. Wait completion of 2nd sequence.
            device.synchronize()
            # b. Free 2nd sequence.
            sequence_id_2 = 2 * self.nb_cycles + 1
            nb_frames = min(self.sequence_size, self.nb_frames - sequence_id_2 * self.sequence_size)
            sequence_2 = pyalp.sequence.Film(sequence_id_2, self.bin_pathname, self.frame_ids, nb_frames,
                                             self.sequence_size, self.rate)
            device.allocate(sequence_2)
            sequence_2.control_timing()
            sequence_2.load()
            sequence_2.start()
            gc.collect()

        # 5. Clean up.
        try:
            device.wait()
            sequence_1.free()
            sequence_2.free()
        except AttributeError:
            pass

        return
