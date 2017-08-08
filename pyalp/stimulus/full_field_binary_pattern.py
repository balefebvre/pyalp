import pyalp.utils
import pyalp.sequence

from .base import Stimulus


class FullFieldBinaryPattern(Stimulus):
    """Full-field binary pattern stimulus.

    Parameters
    ----------
    pattern: list or string, optional
        Definition of the binary pattern either directly by a list of booleans or integers or indirectly by reference to
        a .csv file which contains the description of the pattern.
    rate: float, optional
        Frame rate [Hz]. The default value is 1.0.
    nb_repetitions: integer, optional
        Number of repetitions. The default value is 1 (i.e. stimulus is displayed once).
    interactive: boolean, optional
        Specify if it should prompt the input parameters. The default value is True.
    verbose: boolean, optional
        Verbose mode. The default value is False.

    """
    # TODO complete docstring.

    def __init__(self, pattern=None, rate=1.0, nb_repetitions=1, interactive=False, verbose=False):

        Stimulus.__init__(self)

        if pattern is None:
            pattern = [True, False]

        self.pattern = pattern
        self.rate = rate
        self.nb_repetitions = nb_repetitions

        if interactive:

            self.prompt_input_arguments()

        if verbose:

            self.print_settings()

    def prompt_input_arguments(self, sep=""):
        """Prompt input arguments.

        Parameter
        ---------
        sep: string, optional
            Separator. The default value is \"\"

        """

        print(sep)

        # Prompt binary pattern.
        prompt = "Enter path to the .csv file which contains the description of the binary pattern: "
        self.pattern = pyalp.utils.input(prompt, lambda arg: arg)

        print(sep)

        # Prompt frame rate.
        prompt = "Enter frame rate [Hz] (e.g. {}): ".format(self.rate)
        self.rate = pyalp.utils.input(prompt, float)

        print(sep)

        # Prompt number of repetitions.
        prompt = "Enter number of repetitions (e.g. {}): ".format(self.nb_repetitions)
        self.nb_repetitions = pyalp.utils.input(prompt, float)

        print(sep)

        return

    def print_settings(self):
        """Print settings."""

        raise NotImplementedError()  # TODO implement.

    def display(self, device, verbose=False):
        """Display stimulus.

        Parameter
        ---------
        device: Device
            ALP device.
        verbose: boolean, optional
            Verbosity mode. The default values is False.

        """

        # Define the sequence of frames.
        sequence = pyalp.sequence.FullFieldBinaryPattern(self.pattern, self.rate)
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
