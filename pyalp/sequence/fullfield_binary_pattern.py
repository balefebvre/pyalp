import numpy
import pandas

from .base import Sequence


class FullFieldBinaryPattern(Sequence):
    """Full-field binary pattern sequence

    Parameters
    ----------
    binary_pattern: list or string
    rate: float
        Frame rate [Hz].

    """
    # TODO complete docstring.

    def __init__(self, binary_pattern, rate):
        # Format binary pattern.
        binary_pattern = self.format_binary_pattern(binary_pattern)
        # Initialize sequence.
        bit_planes = 1  # bit depth of the pictures
        pic_num = len(binary_pattern)  # number of pictures
        picture_time = int(1.0e+6 / rate)
        Sequence.__init__(self, bit_planes, pic_num, picture_time=picture_time)
        # Save input parameters.
        self.binary_pattern = binary_pattern
        self.rate = rate

    @staticmethod
    def format_binary_pattern(binary_pattern):
        """Format binary pattern."""

        if isinstance(binary_pattern, str):
            # Extract binary pattern from .csv file.
            dataframe = pandas.read_csv(binary_pattern, sep=';')
            binary_pattern = dataframe['bit'].values

        binary_pattern = [255 if bit else 0 for bit in binary_pattern]
        binary_pattern = numpy.array(binary_pattern, dtype=numpy.uint8)
        binary_pattern = binary_pattern[:, numpy.newaxis, numpy.newaxis]

        return binary_pattern

    def get_user_array(self):
        """Get stimulus frames."""

        width, height = self.device.get_resolution()
        nb_repetitions = (1, height, width)
        frames = numpy.tile(self.binary_pattern, nb_repetitions)

        return frames
