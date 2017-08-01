import numpy as np
import os

import pyalp as alp
import pyalp.utils


class Stimulus(object):
    """TODO add docstring...

    TODO complete...

    """

    def __init__(self):

        pass

    def prompt_input_arguments(self):

        raise NotImplementedError()

    def display(self, device):

        raise NotImplementedError()


class Binary(Stimulus):
    """TODO add docstring.

    Parameters
    ----------
    vec_pathname: string, optional
        Pathname of the .vec file.
    rate: float, optional
        Frame rate [Hz]. The default value is 30.0.
    interactive: bool, optional
        Specify if it should prompt the input parameters. The default value is True.

    TODO complete.

    """

    def __init__(self, vec_pathname="", rate=30.0, nb_repetitions=1, interactive=False):

        Stimulus.__init__(self)

        self.vec_pathname = vec_pathname
        self.rate = rate
        self.nb_repetitions = nb_repetitions
        self.interactive = interactive

        if self.interactive:

            self.prompt_input_arguments()

    def prompt_input_arguments(self):
        """TODO add docstring."""

        raise NotImplementedError()

    def display(self, device):
        """TODO add docstring."""

        # Define images.
        nb_images = 2
        width = device.inquire_display_width()
        height = device.inquire_display_height()
        shape = (nb_images, width, height)
        dtype = np.uint8
        images = np.empty(shape, dtype=dtype)
        images[0, :, :] = np.iinfo(dtype).min
        images[1, :, :] = np.iinfo(dtype).max

        # Define frames.
        nb_frames = int(1.0 * self.rate)
        frames = np.empty(nb_frames, dtype=np.int)
        frames[np.arange(0, nb_frames) % 2 == 0] = 0
        frames[np.arange(0, nb_frames) % 2 == 1] = 1

        # Display available memory before allocation.
        ans = device.inquire_available_memory()
        print("Available memory before allocation [number of binary pictures]: {}".format(ans))

        # Compute picture time.
        picture_time = int(1.0e+6 / self.rate)

        # Define the sequence of frames.
        sequence = None

        # Allocate memory for the sequence of frames.
        device.allocate(sequence)

        # Display available memory after allocation.
        ans = device.inquire_available_memory()
        print("Available memory after allocation [number of binary pictures]: {}".format(ans))

        # Reduce bit depth of the display and suppress dark phase.
        bit_number = 1
        sequence.control_bit_number(bit_number)
        binary_mode = 'uninterrupted'
        sequence.control_binary_mode(binary_mode)

        # Set timing.
        device.timing(sequence)

        # Set up queue mode.
        device.control_projection(queue_mode=True)

        # Transmit pictures into ALP memory.
        device.put(sequence)

        # Start 1st sequence of frames.
        device.start(sequence)

        # Wait.
        device.wait_interruption()

        # return

        raise NotImplementedError()


class Film(Stimulus):
    """TODO add docstring...

    Parameters
    ----------
    bin_pathname: str
        Path name to the .bin file.
    vec_pathname: str
        Path name to the .vec file.
    rate: float
        Frame rate [Hz].
    interactive: bool, optional
        Specify if it should prompt the input parameters. The default value is True.

    """

    dirname = os.path.join("E:", "BINVECS")
    # dirname = os.path.expanduser(os.path.join("~", ".pyalp", "films"))

    def __init__(self, bin_pathname="", vec_pathname="", rate=30.0, nb_lut_frames=200, interactive=True):

        Stimulus.__init__(self)

        self.bin_pathname = bin_pathname
        self.vec_pathname = vec_pathname
        self.rate = rate
        self.nb_lut_frames = nb_lut_frames

        if interactive:

            self.prompt_input_arguments()

    def prompt_input_arguments(self):
        """Prompt the input arguments."""

        sep = ""

        print("# Film stimulus")

        print(sep)

        # Print all the user directories.
        user_dirnames = os.listdir(self.dirname)
        for user_dirname_id, user_dirname in enumerate(user_dirnames):
            print("  {}. {}".format(user_dirname_id, user_dirname))
        # Prompt user identifier.
        user_id = alp.utils.input("Enter the user number (e.g. 0): ", int)
        user_dirname = user_dirnames[user_id]
        user_pathname = os.path.join(self.dirname, user_dirname)

        print(sep)

        # Print all the .bin files.
        bin_pathname = os.path.join(user_pathname, "Bin")
        bin_filenames = [name for name in os.listdir(bin_pathname) if os.path.isfile(os.path.join(bin_pathname, name))]
        for bin_filename_id, bin_filename in enumerate(bin_filenames):
            print("  {}. {}".format(bin_filename_id, bin_filename))
        # Prompt .bin filename identifier.
        bin_id = alp.utils.input("Enter the .bin file number (e.g. 0): ", int)
        bin_filename = bin_filenames[bin_id]
        self.bin_pathname = os.path.join(bin_pathname, bin_filename)

        print(sep)

        # Print all the .vec files.
        vec_pathname = os.path.join(user_pathname, "Vec")
        vec_filenames = [name for name in os.listdir(vec_pathname) if os.path.isfile(os.path.join(vec_pathname, name))]
        for vec_filename_id, vec_filename in enumerate(vec_filenames):
            print("  {}. {}".format(vec_filename_id, vec_filename))
        # Prompt .vec filename identifier.
        vec_id = alp.utils.input("Enter the .vec file number (e.g. 0): ", int)
        vec_filename = vec_filenames[vec_id]
        self.vec_pathname = os.path.join(vec_pathname, vec_filename)

        print(sep)

        # Prompt the frame rate.
        self.rate = alp.utils.input("Enter the frame rate [Hz] (e.g. {}): ".format(self.rate), float)

        print(sep)

        # Prompt the advanced features.
        advanced = alp.utils.input("Advanced features (y/n): ", lambda arg: arg == "y")

        if advanced:
            # Prompt the number of frames in the look up table.
            prompt = "Number of frames in the look up table (e.g. {}): ".format(self.nb_lut_frames)
            callback = int
            self.nb_lut_frames = alp.utils.input(prompt, callback)

        print(sep)

        # Display input arguments.
        print(".vec pathname: {}".format(self.vec_pathname))
        print(".bin pathname: {}".format(self.bin_pathname))
        print("frame rate [Hz]: {}".format(self.rate))
        if advanced:
            print("number of frames in the look up table: {}".format(self.nb_lut_frames))

        print(sep)

        return

    def display(self, device):
        """TODO add docstring."""

        # Read .vec file.
        frame_ids = alp.io.load_vec(self.vec_pathname)
        nb_vec_frames = len(frame_ids)
        print("Number of .vec frames: {}".format(nb_vec_frames))
        print(".vec frame identifiers: {}".format(frame_ids))

        # Read header of .bin file.
        bin_header = alp.io.load_bin_header(self.bin_pathname)
        print(".bin header: {}".format(bin_header))

        # Allocate 1st sequence of frames.
        sequence_1 = None
        device.allocate(sequence_1)
        # TODO 3. Allocate 1st sequence of frames.

        # Allocate 2nd sequence of frames.
        sequence_2 = None
        device.allocate(sequence_2)
        # TODO 4. Allocate 2nd sequence of frames.

        # TODO 5. Play 1st and 2nd sequences on DMD.

        # TODO 6. Repeat step 3., 4. and 5.

        # TODO 7. Wait for key stroke.

        raise NotImplementedError()
