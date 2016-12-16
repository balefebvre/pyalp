import ctypes
import os
import os.path

from . import cst
from . import utils



_alp_path = os.path.join("C:\\", "Program Files", "ALP-4.2")
# _path = os.path.join(_alp_path, "ALP-4.2 basic API", "x64", "alpV42basic.dll") # basic API
_path = os.path.join(_alp_path, "ALP-4.2 high-speed API", "x64", "alpV42.dll") # high-speed API
_device_number = ctypes.c_long(cst.ALP_DEFAULT)


function_names = [
    'AlpDevAlloc',
    'AlpDevControl',
    'AlpDevInquire',
    'AlpDevControlEx',
    'AlpDevHalt',
    'AlpDevFree',
    'AlpSeqAlloc',
    'AlpSeqControl',
    'AlpSeqTiming',
    'AlpSeqInquire',
    'AlpSeqPut',
    'AlpSeqFree',
    'AlpProjControl',
    'AlpProjInquire',
    'AlpProjControlEx',
    'AlpProjInquireEx',
    'AlpProjStart',
    'AlpProjStartCont',
    'AlpProjHalt',
    'AlpProjWait',
    'AlpLedAlloc',
    'AlpLedFree',
    'AlpLedControl',
    'AlpLedInquire',
    'AlpLedControlEx',
    'AlpLedInquireEx',
]


class AlpApi(object):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, path):
        '''TODO add doc...'''
        self.path = path
        self.dll = ctypes.cdll.LoadLibrary(self.path)

    def __getattribute__(self, name):
        '''TODO add doc...'''
        if name in function_names:
            attribute = object.__getattribute__(self.dll, name)
        else:
            attribute = object.__getattribute__(self, name)
        return attribute

    def free(self):
        '''TODO add doc...'''
        del self.dll
        return


class Api(AlpApi):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, path):
        AlpApi.__init__(self, path)
        # TODO swap following lines...
        self.device_id = ctypes.c_ulong(cst.ALP_DEFAULT)
        # self.current_device_id = cst.ALP_DEFAULT
        self.dmd_type = ctypes.c_long(cst.ALP_DEFAULT)
        # TODO swap following lines...
        self.sequence_id = cst.ALP_DEFAULT
        # self.current_sequence_id = cst.ALP_DEFAULT

    def initialize(self, device_number=_device_number):
        # Allocate the ALP high-speed device
        DeviceNumber = ctypes.c_long(device_number)
        InitFlag = ctypes.c_long(self.ALP_DEFAULT)
        DeviceIdPtr = ctypes.byref(self.device_id)
        ret_val = self.AlpDevAlloc(DeviceNumber, InitFlag, DeviceIdPtr)
        # TODO check returned value...
        # Inquire DMD type
        DeviceId = self.device_id
        InquireType = ctypes.c_long(self.ALP_DEV_DMDTYPE)
        UserVarPtr = ctypes.byref(self.dmd_type)
        ret_val = self.AlpDevInquire(DeviceId, InquireType, UserVarPtr)
        # TODO check returned value...
        # Retrieve DMD resolution
        DMDType = self.dmd_type.value
        if DMDType in [ALP_DMDTYPE_XGA, ALP_DMDTYPE_XGA_055A, ALP_DMDTYPE_XGA_055X, ALP_DMDTYPE_XGA_07A]:
            self.dmd_width = 1024 # px
            self.dmd_height = 768 # px
        elif DMDType in [ALP_DMDTYPE_SXGA_PLUS]:
            self.dmd_width = 1400 # px
            self.dmd_height = 1050 # px
        elif DMDType in [ALP_DMDTYPE_DISCONNECT, ALP_DMDTYPE_1080P_095A]:
            self.dmd_width = 1920 # px
            self.dmd_height = 1080 # px
        elif DMDType in [ALP_DMDTYPE_WUXGA_096A]:
            self.dmd_width = 1920 # px
            self.dmd_height = 1200 # px
        elif DMDType in [ALP_DMDTYPE_WQXGA_400MHZ_090A, ALP_DMDTYPE_WQXGA_480MHZ_090A]:
            self.dmd_width = 2560 # px
            self.dmd_height = 1600 # px
        else:
            raise ValueError("Unknown DMD type {}!".format(DMDType))
        return

    # TODO remove following...
    # def display(self, seq):
    #     seq.initialize()
    #     DeviceId = self.device_id
    #     self.AlpProjWait(DeviceId)
    #     seq.finalize()
    #     return

    def finalize(self):
        # Deallocate the ALP high-speed device
        DeviceId = self.device_id
        ret_val = self.AlpDevFree(DeviceId)
        # TODO check returned value...
        del self.dll
        return

    def wait():
        DeviceId = self.device_id
        ret_val = self.AlpProjWait(DeviceId)
        print("AlpSeqAlloc: {}".format(ret_val)) # TODO check returned value...
        return

    # def allocate_sequence(self, bit_planes, pic_num):
    #     DeviceId = self.device_id
    #     BitPlanes = ctypes.c_long(bit_planes)
    #     PicNum = ctyps.c_long(pic_num)
    #     SequenceId = ctypes.c_ulong(cst.ALP_DEFAULT)
    #     SequenceIdPtr = ctypes.byref(SequenceId)
    #     ret_val = self.AlpSeqAlloc(DeviceId, BitPlanes, PicNum, SequenceIdPtr)
    #     print("AlpSeqAlloc: {}".format(ret_val)) # TODO check returned value...
    #     self.sequence_id = SequenceId.value
    #     return
    #
    # def control_sequence(self, control_type, control_value):
    #     raise NotImplementedError()

    def allocate_sequence(self, bit_planes, pic_num):
        sequence = Sequence(self.device_id, bit_planes, pic_num)
        return sequence

    def display_white_sequence(self, seq_repeat=cst.ALP_DEFAULT):
        '''TODO complete...'''
        DeviceId = self.device_id
        # Allocate sequence
        bit_planes = 1
        pic_num = 1
        self.allocate_sequence(bit_planes, pic_num)

        SequenceId = ctypes.c_ulong(self.sequence_id)
        # Control sequence
        ControlType = ctypes.c_long(cst.ALP_SEQ_REPEAT)
        ControlValue = ctypes.c_long(seq_repeat) # between 1 and 1_048_576
        ret_val = self.AlpSeqControl(DeviceId, SequenceId, ControlType, ControlValue)
        print("AlpSeqControl: {}".format(ret_val)) # TODO check returned value...
        # Put sequence
        PicOffset = 0
        PicLoad = 0
        UserArray = utils.get_white_frame(self.dmd_width, self.dmd_height)
        UserArrayPtr = ctypes.cast(UserArray, cast.c_void_p)
        ret_val = self.AlpSeqPut(DeviceId, SequenceId, PicOffset, PicLoad, UserArrayPtr)
        print("AlpSeqPut: {}".format(ret_val)) # TODO check returned value...
        # Set timing
        IlluminateTime = ctypes.c_long(cst.ALP_DEFAULT)
        PictureTime = ctypes.c_long(cst.ALP_DEFAULT)
        SynchDelay = ctypes.c_long(cst.ALP_DEFAULT)
        SynchPulseWidth = ctypes.c_long(cst.ALP_DEFAULT)
        TriggerInDelay = ctypes.c_long(cst.ALP_DEFAULT)
        ret_val = self.AlpSeqTiming(DeviceId, SequenceId, IlluminateTime, PictureTime, SynchDelay, SynchPulseWidth, TriggerInDelay)
        print("AlpSeqTiming: {}".format(ret_val)) # TODO check returned value...
        # Start sequence
        ret_val = self.AlpProjStart(DeviceId, SequenceId) # finite loop
        # ret_val = self.AlpProjStartCont(DeviceId, SequenceId) # infinite loop
        print("AlpProjStart: {}".format(ret_val)) # TODO check returned value...
        # Return sequence identifier
        sequence_id = SequenceId.value
        return sequence_id

    def display_black_sequence(self, seq_repeat=cst.ALP_DEFAULT):
        '''TODO complete...'''
        DeviceId = self.device_id
        SequenceId = ctypes.c_ulong(cst.ALP_DEFAULT)
        # Allocate sequence
        BitPlanes = ctypes.c_long(1)
        PicNum = ctypes.c_long(1)
        SequenceIdPtr = ctypes.byref(SequenceId)
        ret_val = self.AlpSeqAlloc(DeviceId, BitPlanes, PicNum, SequenceIdPtr)
        print("AlpSeqAlloc: {}".format(ret_val)) # TODO check returned value...
        # Control sequence
        ControlType = ctypes.c_long(cst.ALP_SEQ_REPEAT)
        ControlValue = ctypes.c_long(seq_repeat) # between 1 and 1_048_576
        ret_val = self.AlpSeqControl(DeviceId, SequenceId, ControlType, ControlValue)
        print("AlpSeqControl: {}".format(ret_val)) # TODO check returned value...
        # Put sequence
        PicOffset = 0
        PicLoad = 0
        UserArray = utils.get_black_frame(self.dmd_width, self.dmd_height)
        UserArrayPtr = ctypes.cast(UserArray, cast.c_void_p)
        ret_val = self.AlpSeqPut(DeviceId, SequenceId, PicOffset, PicLoad, UserArrayPtr)
        print("AlpSeqPut: {}".format(ret_val)) # TODO check returned value...
        # Set timing
        IlluminateTime = ctypes.c_long(cst.ALP_DEFAULT)
        PictureTime = ctypes.c_long(cst.ALP_DEFAULT)
        SynchDelay = ctypes.c_long(cst.ALP_DEFAULT)
        SynchPulseWidth = ctypes.c_long(cst.ALP_DEFAULT)
        TriggerInDelay = ctypes.c_long(cst.ALP_DEFAULT)
        ret_val = self.AlpSeqTiming(DeviceId, SequenceId, IlluminateTime, PictureTime, SynchDelay, SynchPulseWidth, TriggerInDelay)
        print("AlpSeqTiming: {}".format(ret_val)) # TODO check returned value...
        # Start sequence
        ret_val = self.AlpProjStart(DeviceId, SequenceId) # finite loop
        # ret_val = self.AlpProjStartCont(DeviceId, SequenceId) # infinite loop
        print("AlpProjStart: {}".format(ret_val)) # TODO check returned value...
        # Return sequence identifier
        sequence_id = SequenceId.value
        return sequence_id

    def display_flicker_sequence(self, seq_repeat=cst.ALP_DEFAULT):
        '''TODO complete...'''
        DeviceId = self.device_id
        SequenceId = ctypes.c_ulong(cst.ALP_DEFAULT)
        # Allocate sequence
        BitPlanes = ctypes.c_long(1)
        PicNum = ctypes.c_long(2)
        SequenceIdPtr = ctypes.byref(SequenceId)
        ret_val = self.AlpSeqAlloc(DeviceId, BitPlanes, PicNum, SequenceIdPtr)
        print("AlpSeqAlloc: {}".format(ret_val)) # TODO check returned value...
        # Control sequence
        ControlType = ctypes.c_long(cst.ALP_SEQ_REPEAT)
        ControlValue = ctypes.c_long(seq_repeat) # between 1 and 1_048_576
        ret_val = self.AlpSeqControl(DeviceId, SequenceId, ControlType, ControlValue)
        print("AlpSeqControl: {}".format(ret_val)) # TODO check returned value...
        # Put sequence
        PicOffset = 0
        PicLoad = 0
        UserArray = utils.get_flicker_frames(self.dmd_width, self.dmd_height)
        UserArrayPtr = ctypes.cast(UserArray, cast.c_void_p)
        ret_val = self.AlpSeqPut(DeviceId, SequenceId, PicOffset, PicLoad, UserArrayPtr)
        print("AlpSeqPut: {}".format(ret_val)) # TODO check returned value...
        # Set timing
        IlluminateTime = ctypes.c_long(cst.ALP_DEFAULT)
        PictureTime = ctypes.c_long(cst.ALP_DEFAULT)
        SynchDelay = ctypes.c_long(cst.ALP_DEFAULT)
        SynchPulseWidth = ctypes.c_long(cst.ALP_DEFAULT)
        TriggerInDelay = ctypes.c_long(cst.ALP_DEFAULT)
        ret_val = self.AlpSeqTiming(DeviceId, SequenceId, IlluminateTime, PictureTime, SynchDelay, SynchPulseWidth, TriggerInDelay)
        print("AlpSeqTiming: {}".format(ret_val)) # TODO check returned value...
        # Start sequence
        ret_val = self.AlpProjStart(DeviceId, SequenceId) # finite loop
        # ret_val = self.AlpProjStartCont(DeviceId, SequenceId) # infinite loop
        print("AlpProjStart: {}".format(ret_val)) # TODO check returned value...
        # Return sequence identifier
        sequence_id = SequenceId.value
        return sequence_id

    def display_full_field_sequence(self, fingerprint):
        '''TODO complete...'''
        # TODO do not put the same frame mutiple times on the DMD...
        pic_num = fingerprint.shape[0]
        DeviceId = self.device_id
        SequenceId = ctypes.c_ulong(cst.ALP_DEFAULT)
        # Allocate sequence
        BitPlanes = ctypes.c_long(8)
        PicNum = ctypes.c_long(pic_num)
        SequenceIdPtr = ctypes.byref(SequenceId)
        ret_val = self.AlpSeqAlloc(DeviceId, BitPlanes, PicNum, SequenceIdPtr)
        print("AlpSeqAlloc: {}".format(ret_val)) # TODO check returned value...
        # Put sequence
        PicOffset = 0
        PicLoad = 0
        UserArray = utils.get_full_field_frames(fingerprint, self.dmd_width, self.dmd_height)
        UserArrayPtr = ctypes.cast(UserArray, cast.c_void_p)
        ret_val = self.AlpSeqPut(DeviceId, SequenceId, PicOffset, PicLoad, UserArrayPtr)
        print("AlpSeqPut: {}".format(ret_val)) # TODO check returned value...
        # Set timing
        IlluminateTime = ctypes.c_long(cst.ALP_DEFAULT)
        PictureTime = ctypes.c_long(cst.ALP_DEFAULT)
        SynchDelay = ctypes.c_long(cst.ALP_DEFAULT)
        SynchPulseWidth = ctypes.c_long(cst.ALP_DEFAULT)
        TriggerInDelay = ctypes.c_long(cst.ALP_DEFAULT)
        ret_val = self.AlpSeqTiming(DeviceId, SequenceId, IlluminateTime, PictureTime, SynchDelay, SynchPulseWidth, TriggerInDelay)
        print("AlpSeqTiming: {}".format(ret_val)) # TODO check returned value...
        # Start sequence
        ret_val = self.AlpProjStart(DeviceId, SequenceId) # finite loop
        # ret_val = self.AlpProjStartCont(DeviceId, SequenceId) # infinite loop
        print("AlpProjStart: {}".format(ret_val)) # TODO check returned value...
        # Return sequence identifier
        sequence_id = SequenceId.value
        return sequence_id

    def display_moving_bars(self):
        '''TODO complete...'''
        # TODO find a way to reuse the frames (e.g. forward-backward)...
        DeviceId = self.device_id
        SequenceId = ctypes.c_ulong(cst.ALP_DEFAULT)
        # Allocate sequence
        BitPlanes = ctypes.c_long(1)
        PicNum = ctypes.c_long(0) # TODO correct...
        SequenceIdPtr = ctypes.byref(SequenceId)
        ret_val = self.AlpSeqAlloc(DeviceId, BitPlanes, PicNum, SequenceIdPtr)
        print("AlpSeqAlloc: {}".format(ret_val)) # TODO check returned value...
        # Put sequence
        PicOffset = 0
        PicLoad = 0
        UserArray = utils.get_moving_bars_frames(self.dmd_width, self.dmd_height)
        UserArrayPtr = ctypes.cast(UserArray, cast.c_void_p)
        ret_val = self.AlpSeqPut(DeviceId, SequenceId, PicOffset, PicLoad, UserArrayPtr)
        print("AlpSeqPut: {}".format(ret_val)) # TODO check returned value...
        # Set timing
        IlluminateTime = ctypes.c_long(cst.ALP_DEFAULT)
        PictureTime = ctypes.c_long(cst.ALP_DEFAULT)
        SynchDelay = ctypes.c_long(cst.ALP_DEFAULT)
        SynchPulseWidth = ctypes.c_long(cst.ALP_DEFAULT)
        TriggerInDelay = ctypes.c_long(cst.ALP_DEFAULT)
        ret_val = self.AlpSeqTiming(DeviceId, SequenceId, IlluminateTime, PictureTime, SynchDelay, SynchPulseWidth, TriggerInDelay)
        print("AlpSeqTiming: {}".format(ret_val)) # TODO check returned value...
        # Start sequence
        ret_val = self.AlpProjStart(DeviceId, SequenceId) # finite loop
        # ret_val = self.AlpProjStartCont(DeviceId, SequenceId) # infinite loop
        print("AlpProjStart: {}".format(ret_val)) # TODO check returned value...
        # Return sequence identifier
        sequence_id = SequenceId.value
        return sequence_id

    def display_binary_dense_noise(self):
        '''TODO add doc...'''
        # TODO understand why 'dense'...
        raise NotImplementedError()

    def allocate_device(self, device_number=_device_number):
        '''Allocate device'''
        device = Device(self, device_number)
        return device
