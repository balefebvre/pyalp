import gc
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


class Rectangle(Stimulus):
    """Rectangle stimulus.

    Parameters
    ----------
    x: float, optional
        x-coordinate of the center of the rectangle [um]. The default value is +0.0.
    y: float, optional
        y-coordinate of the center of the rectangle [usm]. The default value is +0.0.
    w: float, optional
        Width of the rectangle [um]. The default value is 300.0.
    h: float, optional
        Height of the rectangle [um]. The default value is 300.0.
    alpha: float, optional
        Pixel size [um]. The default value is 2.3.
    rate: float, optional
        Frame rate [Hz]. The default value is 40.0.
    duration: float, optional
        Stimulus duration [s]. The default value is 20.0.
    interactive: boolean, optional
        The default value is False.
    verbose: boolean, optional
        The default value is False.

    """

    def __init__(self, x=0.0, y=0.0, w=300.0, h=300.0, alpha=2.3, rate=40.0, duration=20.0, interactive=False, verbose=False):

        Stimulus.__init__(self)

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.alpha = alpha
        self.rate = rate
        self.duration = duration

        if interactive:

            self.prompt_input_arguments()

        self.nb_frames = int(self.rate * self.duration)
        self.nb_repetitions = self.nb_frames

        if verbose:

            self.print_settings()

    def prompt_input_arguments(self, sep=""):
        """Prompt input arguments."""

        # Prompt x-coordinate of the center.
        prompt = "Enter the x-coordinate of the center of the rectangle [um] (e.g. {}): ".format(self.x)
        self.x = alp.utils.input(prompt, float)

        # Prompt y-coordinate of the center.
        prompt = "Enter the y-coordinate of the center of the rectangle [um] (e.g. {}): ".format(self.y)
        self.y = alp.utils.input(prompt, float)

        # Prompt rectangle width.
        prompt = "Enter the width of the rectangle [um] (e.g. {}): ".format(self.w)
        self.w = alp.utils.input(prompt, float)

        # Prompt rectangle height.
        prompt = "Enter the height of the rectangle [um] (e.g. {}): ".format(self.h)
        self.h = alp.utils.input(prompt, float)

        # Prompt pixel size.
        prompt = "Enter the pixel size [um] (e.g. {}): ".format(self.alpha)
        self.alpha = alp.utils.input(prompt, float)

        # Prompt frame rate.
        prompt = "Enter frame rate [Hz] (e.g. {}): ".format(self.rate)
        self.rate = alp.utils.input(prompt, float)

        # Prompt stimulus duration.
        prompt = "Enter stimulus duration [s] (e.g. {}): ".format(self.duration)
        self.duration = alp.utils.input(prompt, float)

        return

    def print_settings(self):
        """Print settings."""

        print("--------------- Rectangle stimulus ---------------")
        print("x-coordinate: {} um".format(self.x))
        print("y-coordinate: {} um".format(self.y))
        print("width: {} um".format(self.w))
        print("height: {} um".format(self.h))
        print("pixel size: {} um".format(self.alpha))
        print("frame rate: {} Hz".format(self.rate))
        print("duration: {} s".format(self.duration))
        print("--------------------------------------------------")
        print("")

        return

    def display(self, device, verbose=False):
        """Display stimulus.

        Parameter
        ---------
        device: Device
            ALP device.
        verbose: boolean, optional
            Verbosity mode. The default value is False.

        """

        # Define the sequence of frames.
        sequence = alp.sequence.Rectangle(self.x, self.y, self.w, self.h, self.alpha, self.rate)
        # Display available memory before allocation.
        if verbose:
            ans = device.inquire_available_memory()
            print("Available memory before allocation [number of binary pictures]: {}".format(ans))
        # Allocate memory for the sequence of frames.
        device.allocate(sequence)
        # Display available memory after allocation.
        if verbose:
            ans = device.inquire_available_memory()
            print("Available memory after allocation [number of binary pictures]: {}".format(ans))
        # Control the bit depth of the sequence display.
        sequence.control_bit_number(1)
        # Control the number of repetitions of the sequence display.
        sequence.control_nb_repetitions(self.nb_repetitions)
        # Control the dark phase property of the sequence display.
        sequence.control_binary_mode('uninterrupted')
        # Control the timing properties of the sequence display.
        sequence.control_timing()
        # Transmit the sequence of frames into memory.
        sequence.load()
        # Start the sequence of frames.
        sequence.start()
        # Wait.
        device.wait()
        # Free the sequence of frames.
        sequence.free()

        return


class FullFieldBinaryPattern(Stimulus):
    """TODO add docstring.

    Parameters
    ----------
    pattern: list or string, optional
        Definition of the binary pattern either directly by a list of booleans or integers or indirectly by reference to
        a .csv file which contains the description of the pattern.
    rate: float, optional
        Frame rate [Hz]. The default value is 1.0.
    nb_repetitions: integer, optional
        Number of repetitions. The default value is 1 (i.e. stimulus is displayed once).
    interactive: bool, optional
        Specify if it should prompt the input parameters. The default value is True.

    TODO complete.

    """

    def __init__(self, pattern=None, rate=1.0, nb_repetitions=1, interactive=False):

        Stimulus.__init__(self)

        if pattern is None:
            pattern = [True, False]

        self.pattern = pattern
        self.rate = rate
        self.nb_repetitions = nb_repetitions
        self.interactive = interactive

        if self.interactive:

            self.prompt_input_arguments()

    def prompt_input_arguments(self):
        """Prompt input arguments."""
        # TODO complete docstring.

        raise NotImplementedError()

    def display(self, device, verbose=False):
        """Display stimulus.

        Parameter
        ---------
        device: Device
            ALP device.
        verbose: boolean, optional
            Verbosity mode. The default values is False.

        """
        # TODO complete docstring.

        # Define the sequence of frames.
        sequence = alp.sequence.FullFieldBinaryPattern(self.pattern, self.rate)

        if verbose:
            # Display available memory before allocation.
            ans = device.inquire_available_memory()
            print("Available memory before allocation [number of binary pictures]: {}".format(ans))

        # Allocate memory for the sequence of frames.
        device.allocate(sequence)

        if verbose:
            # Display available memory after allocation.
            ans = device.inquire_available_memory()
            print("Available memory after allocation [number of binary pictures]: {}".format(ans))

        # Control the bit depth of the sequence display.
        sequence.control_bit_number(1)

        # Control the number of repetitions of the sequence display.
        sequence.control_nb_repetitions(self.nb_repetitions)

        # Control the dark phase property of the sequence display.
        sequence.control_binary_mode('uninterrupted')

        # Control the timing properties of the sequence display.
        sequence.control_timing()

        # Transmit the sequence of frames into memory.
        sequence.load()

        # Start the sequence of frames.
        sequence.start()

        # Wait.
        device.wait()

        return


class Checkerboard(Stimulus):
    """Checkerboard stimulus

    Parameters
    ----------
    check_size: integer, optional
        Check size [px]. The default value is 18.
    nb_checks: integer, optional
        Number of checks. The default value is 20.
    rate: float, optional
        Frame rate [Hz]. The default value is 30.0.
    duration: float optional
        Stimulus durations [s]. The default value is 5.0.
    sequence_size: integer, optional
        Number of frames per sequence. High numbers enable high frame rate but increase memory consumption. The default
        value is 250.
    interactive: boolean, optional
        The default value is False.
    verbose: boolean, optional
        The default value is False.

    """

    def __init__(self, check_size=18, nb_checks=20, rate=30.0, duration=5.0, sequence_size=250,
                 interactive=False, verbose=False):

        Stimulus.__init__(self)

        self.check_size = check_size
        self.nb_checks = nb_checks
        self.rate = rate
        self.duration = duration
        self.sequence_size = sequence_size  # i.e. number of frames

        if interactive:
            self.prompt_input_arguments()

        self.nb_frames = int(self.rate * self.duration)
        self.nb_sequences = int(self.nb_frames / self.sequence_size)
        self.nb_cycles = int(self.nb_sequences / 2)

        if verbose:
            self.print_settings()

        # TODO manage remaining frames as a partial sequence.

    def prompt_input_arguments(self, sep=""):
        """Prompt input arguments."""
        # TODO complete docstring.

        # Prompt check size.
        prompt = "Enter the number of pixels to make one side of a check (e.g. {}): ".format(self.check_size)
        self.check_size = alp.utils.input(prompt, int)

        print(sep)

        # Prompt number of checks.
        prompt = "Enter the number of checks to make one side of the checkerboard (e.g. {}): ".format(self.nb_checks)
        self.nb_checks = alp.utils.input(prompt, int)

        print(sep)

        # Prompt frame rate.
        prompt = "Enter the frame rate (e.g. {}): ".format(self.rate)
        self.rate = alp.utils.input(prompt, float)

        print(sep)

        # Prompt duration.
        prompt = "Enter the duration [s] (e.g. {}): ".format(self.duration)
        self.duration = alp.utils.input(prompt, float)

        print(sep)

        # Prompt advanced features.
        prompt = "Advanced features (y/n): "
        advanced = alp.utils.input(prompt, lambda arg: arg == "y")

        print(sep)

        if advanced:

            # Prompt sequence size.
            prompt = "Enter the sequence size (e.g. {}): ".format(self.sequence_size)
            self.sequence_size = alp.utils.input(prompt, int)

            print(sep)

        return

    def print_settings(self):
        """Print settings."""

        print("------------- Checkerboard stimulus --------------")
        print("check size: {} px".format(self.check_size))
        print("number of checks: {}".format(self.nb_checks))
        print("rate: {} Hz".format(self.rate))
        print("duration: {} s".format(self.duration))
        print("sequence size: {}".format(self.sequence_size))
        print("number of frames: {}".format(self.nb_frames))
        print("number of sequences: {}".format(self.nb_sequences))
        print("number of cycles: {}".format(self.nb_cycles))
        print("--------------------------------------------------")
        print("")

        return

    def display(self, device, verbose=False):
        """Display stimulus.

        Parameters
        ----------
        device: Device
            ALP device.
        verbose: boolean, optional
            The default value is False.

        """
        # TODO complete docstring.

        sequence_1 = None
        sequence_2 = None

        if self.nb_frames > 0 * self.sequence_size:  # i.e. enough frames

            # 1. Allocate 1st sequence of frames.
            # Define 1st sequence of frames.
            sequence_id_1 = 0
            if self.nb_frames > 1 * self.sequence_size:
                nb_frames = self.sequence_size
            else:
                nb_frames = self.nb_frames - 0 * self.sequence_size
            sequence_1 = alp.sequence.CheckerboardBis(sequence_id_1, self.check_size, self.nb_checks,
                                                      nb_frames, self.rate)
            # Display available memory before allocation of 1st sequence.
            if verbose:
                ans = device.inquire_available_memory()
                print("Available memory before allocation of 1st sequence [number of binary pictures]: {}".format(ans))
            # Allocate memory for 1st sequence of frames.
            device.allocate(sequence_1)
            # Display available memory after allocation of 1st sequence.
            if verbose:
                ans = device.inquire_available_memory()
                print("Available memory after allocation of 1st sequence [number of binary pictures]: {}".format(ans))
            # Control the bit depth of 1st sequence display.
            sequence_1.control_bit_number(1)
            # Control the dark phase property of the sequence display.
            sequence_1.control_binary_mode('uninterrupted')
            # Control the timing properties of 1st sequence display.
            sequence_1.control_timing()

        if self.nb_frames > 1 * self.sequence_size:  # i.e. enough frames

            # 2. Allocate 2nd sequence of frames.
            # Define 2nd sequence of frames.
            sequence_id_2 = 1
            if self.nb_frames > 2 * self.sequence_size:
                nb_frames = self.sequence_size
            else:
                nb_frames = self.nb_frames - 1 * self.sequence_size
            sequence_2 = alp.sequence.CheckerboardBis(sequence_id_2, self.check_size, self.nb_checks,
                                                      nb_frames, self.rate)
            # Display available memory before allocation of 2nd sequence.
            if verbose:
                ans = device.inquire_available_memory()
                print("Available memory before allocation of 2nd sequence [number of binary pictures]: {}".format(ans))
            # Allocate memory for the 2nd sequence of frames.
            device.allocate(sequence_2)
            # Display available memory after allocation of 2nd sequence.
            if verbose:
                ans = device.inquire_available_memory()
                print("Available memory after allocation of 2nd sequence [number of binary pictures]: {}".format(ans))
            # Control the bit depth of 2nd sequence display.
            sequence_2.control_bit_number(1)
            # Control the dark phase property of 2nd sequence display.
            sequence_2.control_binary_mode('uninterrupted')
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
            sequence_1 = alp.sequence.CheckerboardBis(sequence_id_1, self.check_size, self.nb_checks,
                                                      nb_frames, self.rate)
            device.allocate(sequence_1)
            sequence_1.control_bit_number(1)
            sequence_1.control_binary_mode('uninterrupted')
            sequence_1.control_timing()
            sequence_1.load()
            sequence_1.start()
            gc.collect()
            # d. Wait completion of 2nd sequence.
            device.synchronize()
            # e. Free 2nd sequence.
            sequence_2.free()
            # f. Reallocate 2nd sequence of frames.
            sequence_id_2 = 2 * cycle_id + 1
            nb_frames = self.sequence_size
            sequence_2 = alp.sequence.CheckerboardBis(sequence_id_2, self.check_size, self.nb_checks,
                                                      nb_frames, self.rate)
            device.allocate(sequence_2)
            sequence_2.control_bit_number(1)
            sequence_2.control_binary_mode('uninterrupted')
            sequence_2.control_timing()
            sequence_2.load()
            sequence_2.start()
            gc.collect()

        if self.nb_frames > (self.nb_cycles * 2 + 0) * self.sequence_size:  # i.e. remaining frames

            # a. Wait completion of 1st sequence.
            device.synchronize()
            # b. Free 1st sequence.
            sequence_1.free()
            # c. Reallocate 1st sequence.
            sequence_id_1 = 2 * self.nb_cycles + 0
            if self.nb_frames > (sequence_id_1 + 1) * self.sequence_size:
                nb_frames = self.sequence_size
            else:
                nb_frames = self.nb_frames - sequence_id_1 * self.sequence_size
            sequence_1 = alp.sequence.CheckerboardBis(sequence_id_1, self.check_size, self.nb_checks,
                                                      nb_frames, self.rate)
            device.allocate(sequence_1)
            sequence_1.control_bit_number(1)
            sequence_1.control_binary_mode('uninterrupted')
            sequence_1.control_timing()
            sequence_1.load()
            sequence_1.start()
            gc.collect()

        if self.nb_frames > (self.nb_cycles * 2 + 1) * self.sequence_size:  # i.e. remaining frames

            # a. Wait completion of 2nd sequence.
            device.synchronize()
            # b. Free 2nd sequence.
            sequence_2.free()
            # c. Reallocate 2st sequence.
            sequence_id_2 = 2 * self.nb_cycles + 1
            if self.nb_frames > (sequence_id_2 + 1) * self.sequence_size:
                nb_frames = self.sequence_size
            else:
                nb_frames = self.nb_frames - sequence_id_2 * self.sequence_size
            sequence_2 = alp.sequence.CheckerboardBis(sequence_id_2, self.check_size, self.nb_checks,
                                                      nb_frames, self.rate)
            device.allocate(sequence_2)
            sequence_2.control_bit_number(1)
            sequence_2.control_binary_mode('uninterrupted')
            sequence_2.control_timing()
            sequence_2.load()
            sequence_2.start()
            gc.collect()

        # 5. Clean up.
        try:
            device.wait()
            sequence_1.free()  # might raise an exception if sequence_1 have not be defined
            sequence_2.free()  # might raise an exception if sequence_2 have not be defined
        except NameError:
            pass

        return


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
        # TODO complete docstring.

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
        """Display stimulus.

        Parameter
        ---------
        device: Device
            ALP device.

        """
        # TODO complete docstring.

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
