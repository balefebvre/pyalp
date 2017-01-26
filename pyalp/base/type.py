from ctypes import Structure, c_ulong



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
