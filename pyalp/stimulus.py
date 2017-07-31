import os

import pyalp as alp
import pyalp.utils


class Stimulus(object):
    """TODO add docstring...

    TODO complete...

    """

    def __init__(self):

        pass


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

    dirname = os.path.expanduser(os.path.join("~", ".pyalp", "films"))

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

        print("# Film stimulus\n")

        # Print all the user directories.
        user_dirnames = os.listdir(self.dirname)
        for user_dirname_id, user_dirname in enumerate(user_dirnames):
            print("  {}. {}".format(user_dirname_id, user_dirname))
        # Prompt user identifier.
        user_id = alp.utils.input("Enter the user number (e.g. 0): ", int)
        user_dirname = user_dirnames[user_id]
        user_pathname = os.path.join(self.dirname, user_dirname)

        # Print all the BIN files.
        bin_pathname = os.path.join(user_pathname, "Bin")
        bin_filenames = [name for name in os.listdir(bin_pathname) if os.path.isfile(os.path.join(bin_pathname, name))]
        for bin_filename_id, bin_filename in enumerate(bin_filenames):
            print("  {}. {}".format(bin_filename_id, bin_filename))
        # Prompt BIN filename identifier.
        bin_id = alp.utils.input("Enter the .bin file number (e.g. 0): ", int)
        bin_filename = bin_filenames[bin_id]
        bin_pathname = os.path.join(bin_pathname, bin_filename)

        # Print all the VEC files.
        vec_pathname = os.path.join(user_pathname, "Vec")
        vec_filenames = [name for name in os.listdir(vec_pathname) if os.path.isfile(os.path.join(vec_pathname, name))]
        for vec_filename_id, vec_filename in enumerate(vec_filenames):
            print("  {}. {}".format(vec_filename_id, vec_filename))
        # Prompt VEC filename identifier.
        vec_id = alp.utils.input("Enter the .vec file number (e.g. 0): ", int)
        vec_filename = vec_filenames[vec_id]
        vec_pathname = os.path.join(vec_pathname, vec_filename)

        # Prompt the frame rate.
        rate = alp.utils.input("Enter the frame rate [Hz] (e.g. {}): ".format(self.rate), float)

        # Prompt the advanced features.
        advanced = alp.utils.input("Advanced features (y/n): ", lambda arg: arg == "y")

        if advanced:
            # Prompt the number of frames in the look up table.
            nb_lut_frames = alp.utils.input("Number of frames in the look up table (e.g. {}): ".format(self.nb_lut_frames),
                                            int)

        self.bin_pathname = ""
        self.vec_pathname = ""
        self.rate = 30.0
        self.nb_lut_frames = 200