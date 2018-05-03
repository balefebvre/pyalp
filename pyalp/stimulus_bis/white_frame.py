from .base import IStimulus
from .sequence.white_frame import WhiteFrameSequence


class WhiteFrameStimulus(IStimulus):

    def __init__(self, height, width, rate, duration):

        self._height = height
        self._width = width
        self._rate = rate
        self._duration = duration

        return

    @property
    def control_items(self):

        return

    @property
    def sequences(self):

        sequence = WhiteFrameSequence(self._height, self._width)

        yield sequence

        return
