import pyalp.utils
import pyalp.sequence

from .base import Stimulus


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

    def __init__(self, x=0.0, y=0.0, w=300.0, h=300.0, alpha=2.3, rate=40.0, duration=20.0,
                 interactive=False, verbose=False):

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
        self.x = pyalp.utils.input(prompt, float)

        print(sep)

        # Prompt y-coordinate of the center.
        prompt = "Enter the y-coordinate of the center of the rectangle [um] (e.g. {}): ".format(self.y)
        self.y = pyalp.utils.input(prompt, float)

        print(sep)

        # Prompt rectangle width.
        prompt = "Enter the width of the rectangle [um] (e.g. {}): ".format(self.w)
        self.w = pyalp.utils.input(prompt, float)

        print(sep)

        # Prompt rectangle height.
        prompt = "Enter the height of the rectangle [um] (e.g. {}): ".format(self.h)
        self.h = pyalp.utils.input(prompt, float)

        print(sep)

        # Prompt pixel size.
        prompt = "Enter the pixel size [um] (e.g. {}): ".format(self.alpha)
        self.alpha = pyalp.utils.input(prompt, float)

        print(sep)

        # Prompt frame rate.
        prompt = "Enter frame rate [Hz] (e.g. {}): ".format(self.rate)
        self.rate = pyalp.utils.input(prompt, float)

        print(sep)

        # Prompt stimulus duration.
        prompt = "Enter stimulus duration [s] (e.g. {}): ".format(self.duration)
        self.duration = pyalp.utils.input(prompt, float)

        print(sep)

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
        sequence = pyalp.sequence.Rectangle(self.x, self.y, self.w, self.h, self.alpha, self.rate)
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
