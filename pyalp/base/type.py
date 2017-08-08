from ctypes import Structure, c_ulong

from .constant import *


class tAlpProjProgress(Structure):

    _fields_ = [
        ('CurrentQueueId', c_ulong),
        ('SequenceId', c_ulong),
        ('nWaitingSequences', c_ulong),
        ('nSequenceCounter', c_ulong),
        ('nSequenceCounterUnderflow', c_ulong),
        ('nFrameCounter', c_ulong),
        ('nPictureTime', c_ulong),
        ('nFramesPerSubSequence', c_ulong),
        ('nFlags', c_ulong),
    ]

    @property
    def is_idle(self):
        """Flag reveals if there are currently no active sequences."""

        return bool(self.nFlags & ALP_FLAG_QUEUE_IDLE)

    @property
    def is_continuous(self):
        """Flag reveals if the running sequence is started continuously."""
        
        return bool(self.nFlags & ALP_FLAG_SEQUENCE_INDEFINITE)
    
    @property
    def is_aborted(self):
        """Flag reveals if the running sequence is about to be aborted."""

        return bool(self.nFlags & ALP_FLAG_SEQUENCE_INDEFINITE)

    @property
    def is_finished(self):
        """Flag reveals if the last frames of a sequence has completed illumination."""

        return bool(self.nFlags & ALP_FLAG_FRAME_FINISHED)
