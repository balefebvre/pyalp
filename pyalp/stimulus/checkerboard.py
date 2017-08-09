import gc

import pyalp.utils
import pyalp.sequence

from .base import Stimulus


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
        self.check_size = pyalp.utils.input(prompt, int)

        print(sep)

        # Prompt number of checks.
        prompt = "Enter the number of checks to make one side of the checkerboard (e.g. {}): ".format(self.nb_checks)
        self.nb_checks = pyalp.utils.input(prompt, int)

        print(sep)

        # Prompt frame rate.
        prompt = "Enter the frame rate (e.g. {}): ".format(self.rate)
        self.rate = pyalp.utils.input(prompt, float)

        print(sep)

        # Prompt duration.
        prompt = "Enter the duration [s] (e.g. {}): ".format(self.duration)
        self.duration = pyalp.utils.input(prompt, float)

        print(sep)

        # Prompt advanced features.
        prompt = "Advanced features (y/n): "
        advanced = pyalp.utils.input(prompt, lambda arg: arg == "y")

        print(sep)

        if advanced:

            # Prompt sequence size.
            prompt = "Enter the sequence size (e.g. {}): ".format(self.sequence_size)
            self.sequence_size = pyalp.utils.input(prompt, int)

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
            sequence_1 = pyalp.sequence.CheckerboardBis(sequence_id_1, self.check_size, self.nb_checks,
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
            sequence_2 = pyalp.sequence.CheckerboardBis(sequence_id_2, self.check_size, self.nb_checks,
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
            sequence_1 = pyalp.sequence.CheckerboardBis(sequence_id_1, self.check_size, self.nb_checks,
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
            sequence_2 = pyalp.sequence.CheckerboardBis(sequence_id_2, self.check_size, self.nb_checks,
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
            sequence_1 = pyalp.sequence.CheckerboardBis(sequence_id_1, self.check_size, self.nb_checks,
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
            sequence_2 = pyalp.sequence.CheckerboardBis(sequence_id_2, self.check_size, self.nb_checks,
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
            sequence_1.free()
            sequence_2.free()
        except AttributeError:
            pass

        return
