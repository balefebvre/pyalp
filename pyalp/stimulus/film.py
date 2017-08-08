import os

import pyalp.io
import pyalp.sequence
import pyalp.utils

from .base import Stimulus


class Film(Stimulus):
    """Film stimulus

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
    # TODO complete docstring.

    dirname = os.path.join("E:", "BINVECS")
    # dirname = os.path.expanduser(os.path.join("~", ".pyalp", "films"))  # TODO remove.

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
        # TODO complete docstring.

        sep = ""

        print("# Film stimulus")

        print(sep)

        # Print all the user directories.
        user_dirnames = os.listdir(self.dirname)
        for user_dirname_id, user_dirname in enumerate(user_dirnames):
            print("  {}. {}".format(user_dirname_id, user_dirname))
        # Prompt user identifier.
        user_id = pyalp.utils.input("Enter the user number (e.g. 0): ", int)
        user_dirname = user_dirnames[user_id]
        user_pathname = os.path.join(self.dirname, user_dirname)

        print(sep)

        # Print all the .bin files.
        bin_pathname = os.path.join(user_pathname, "Bin")
        bin_filenames = [name for name in os.listdir(bin_pathname) if os.path.isfile(os.path.join(bin_pathname, name))]
        for bin_filename_id, bin_filename in enumerate(bin_filenames):
            print("  {}. {}".format(bin_filename_id, bin_filename))
        # Prompt .bin filename identifier.
        bin_id = pyalp.utils.input("Enter the .bin file number (e.g. 0): ", int)
        bin_filename = bin_filenames[bin_id]
        self.bin_pathname = os.path.join(bin_pathname, bin_filename)

        print(sep)

        # Print all the .vec files.
        vec_pathname = os.path.join(user_pathname, "Vec")
        vec_filenames = [name for name in os.listdir(vec_pathname) if os.path.isfile(os.path.join(vec_pathname, name))]
        for vec_filename_id, vec_filename in enumerate(vec_filenames):
            print("  {}. {}".format(vec_filename_id, vec_filename))
        # Prompt .vec filename identifier.
        vec_id = pyalp.utils.input("Enter the .vec file number (e.g. 0): ", int)
        vec_filename = vec_filenames[vec_id]
        self.vec_pathname = os.path.join(vec_pathname, vec_filename)

        print(sep)

        # Prompt the frame rate.
        self.rate = pyalp.utils.input("Enter the frame rate [Hz] (e.g. {}): ".format(self.rate), float)

        print(sep)

        # Prompt the advanced features.
        advanced = pyalp.utils.input("Advanced features (y/n): ", lambda arg: arg == "y")

        if advanced:
            # Prompt the number of frames in the look up table.
            prompt = "Number of frames in the look up table (e.g. {}): ".format(self.nb_lut_frames)
            callback = int
            self.nb_lut_frames = pyalp.utils.input(prompt, callback)

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
        """Display stimulus.

        Parameter
        ---------
        device: Device
            ALP device.

        """
        # TODO complete docstring.

        # Read .vec file.
        frame_ids = pyalp.io.load_vec(self.vec_pathname)
        nb_vec_frames = len(frame_ids)
        print("Number of .vec frames: {}".format(nb_vec_frames))
        print(".vec frame identifiers: {}".format(frame_ids))

        # Read header of .bin file.
        bin_header = pyalp.io.load_bin_header(self.bin_pathname)
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
