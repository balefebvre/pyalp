import numpy as np

from .base import ISequence


class WhiteFrameSequence(ISequence):

    def __init__(self, height, width, number_repetitions):

        self._height = height
        self._width = width

        self._control = dict(
            bit_number=1,
            number_repetitions=1,
            binary_mode='uninterrupted',
            timing=None,
        )

        return

    @property
    def size(self):

        return self.number_pictures * self._height * self._width

    @property
    def bit_planes(self):

        return 8

    @property
    def number_pictures(self):

        return 1

    @property
    def control_items(self):

        return self._control.items()

    @property
    def data(self):

        return np.iinfo(np.uint8).max * np.ones(self.size, dtype=np.uint8)
