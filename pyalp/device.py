import ctypes
from ctypes import c_long, c_ulong, byref, cast

from . import api
from . import utils
from .base.constant import *
from .protocol import Protocol
from .sequence import Sequence



def allocate(device_number=ALP_DEFAULT):
    '''Allocate an ALP hardware system (board set)'''
    device = Device(device_number)
    return device


class Device(object):
    '''TODO add doc...

    TODO complete...
    '''
    def __init__(self, device_number):
        '''Allocate an ALP hardware system (board set)'''
        # Save input parameter
        self.nb = device_number
        # Allocate device
        DeviceNumber = c_long(device_number)
        InitFlag = c_long(ALP_DEFAULT)
        DeviceId = c_ulong(ALP_DEFAULT)
        DeviceIdPtr = byref(DeviceId)
        ret_val = api.AlpDevAlloc(DeviceNumber, InitFlag, DeviceIdPtr)
        if ret_val == ALP_OK:
            self.id = DeviceId.value
        else:
            raise Exception("AlpDevAlloc: {}".format(ret_val))

    def __del__(self):
        '''Deallocate the ALP hardware system (board set)'''
        DeviceId = c_ulong(self.id)
        ret_val = api.AlpDevFree(DeviceId)
        if ret_val == ALP_OK:
            return
        else:
            raise Exception("AlpDevFree: {}".format(ret_val))

    def get_id(self):
        '''Get DMD identifier'''
        # Return DMD identifier
        return self.id

    def get_dmd_type(self):
        '''Get DMD type'''
        # Inquire DMD type
        DeviceId = c_ulong(self.id)
        InquireType = c_long(ALP_DEV_DMDTYPE)
        UserVar = c_long(ALP_DEFAULT)
        UserVarPtr = byref(UserVar)
        ret_val = api.AlpDevInquire(DeviceId, InquireType, UserVarPtr)
        if ret_val == ALP_OK:
            self.dmd_type = UserVar.value
            return self.dmd_type
        else:
            raise Exception("AlpDevInquire: {}".format(ret_val))

    def get_resolution(self):
        '''Get DMD resolution (in pixels)'''
        # Inquire DMD type
        dmd_type = self.get_dmd_type()
        # Retrieve DMD width and height
        # TODO clean following commented lines...
        if dmd_type in [ALP_DMDTYPE_XGA, ALP_DMDTYPE_XGA_055X, ALP_DMDTYPE_XGA_07A]:
        # if dmd_type in [ALP_DMDTYPE_XGA, ALP_DMDTYPE_XGA_055A, ALP_DMDTYPE_XGA_055X, ALP_DMDTYPE_XGA_07A]:
            width = 1024 # px
            height = 768 # px
        # TODO clean following commented lines...
        # elif dmd_type in [ALP_DMDTYPE_SXGA_PLUS]:
        #     width = 1400 # px
        #     height = 1050 # px
        elif dmd_type in [ALP_DMDTYPE_DISCONNECT, ALP_DMDTYPE_1080P_095A]:
            width = 1920 # px
            height = 1080 # px
        elif dmd_type in [ALP_DMDTYPE_WUXGA_096A]:
            width = 1920 # px
            height = 1200 # px
        # TODO clean following commented lines...
        # elif dmd_type in [ALP_DMDTYPE_WQXGA_400MHZ_090A, ALP_DMDTYPE_WQXGA_480MHZ_090A]:
        #     width = 2560 # px
        #     height = 1600 # px
        else:
            raise ValueError("Unknown DMD type {}!".format(self.dmd_type))
        # Save parameters
        self.width = width
        self.height = height
        self.resolution = self.width, self.height
        # Return DMD resolution
        return self.resolution

    def display(self, protocol):
        '''Display protocol'''
        if isinstance(protocol, list): # TODO create a Queue class...
            queue = protocol
            for sequence in queue:
                sequence.display(self)
                if sequence.is_finite():
                    self.wait_completion()
                else:
                    self.wait_interuption()
        elif isinstance(protocol, Protocol):
            protocol.project(self)
        elif isinstance(protocol, Sequence):
            sequence = protocol
            sequence.display(self)
            self.wait()
        else:
            raise NotImplementedError("pyalp.device.display")
        return

    def allocate(self, sequence):
        '''Allocate sequence'''
        DeviceId = c_ulong(self.id)
        BitPlanes = c_long(sequence.bit_planes)
        PicNum = c_long(sequence.pic_num)
        SequenceId = c_ulong(ALP_DEFAULT)
        SequenceIdPtr = byref(SequenceId)
        ret_val = api.AlpSeqAlloc(DeviceId, BitPlanes, PicNum, SequenceIdPtr)
        if ret_val == ALP_OK:
            sequence.id = SequenceId.value
            return
        else:
            raise Exception("AlpSeqAlloc: {}".format(ret_val))

    # def control(self, sequence):
    #     '''Control sequence'''
    #     DeviceId = c_ulong(self.id)
    #     SequenceId = c_ulong(sequence.id)
    #     if sequence.n_repetitions is None:
    #         pass
    #     else:
    #         ControlType = c_long(ALP_SEQ_REPEAT)
    #         ControlValue = c_long(sequence.n_repetitions)
    #         ret_val = api.AlpSeqControl(DeviceId, SequenceId, ControlType, ControlValue)
    #         if ret_val == ALP_OK:
    #             pass
    #         else:
    #             raise Exception("AlpSeqControl: {}".format(ret_val))
    #     # TODO add other controls...
    #     return

    def control(self, sequence, control_type, control_value):
        '''Control sequence'''
        DeviceId = c_ulong(self.id)
        SequenceId = c_ulong(sequence.id)
        ControlType = c_long(control_type)
        ControlValue = c_long(control_value)
        ret_val = api.AlpSeqControl(DeviceId, SequenceId, ControlType, ControlValue)
        if ret_val == ALP_OK:
            return
        else:
            raise Exception("AlpSeqControl: {}".format(ret_val))

    def control_repetitions(self, sequence, nb_repetitions):
        '''Control sequence repetitions'''
        self.control(sequence, ALP_SEQ_REPEAT, nb_repetitions)
        return

    def timing(self, sequence):
        '''Set sequence timing'''
        # TODO avoid set timing if possible (i.e. only default values)...
        DeviceId = c_ulong(self.id)
        IlluminateTime = c_long(sequence.illuminate_time)
        PictureTime = c_long(sequence.picture_time)
        SynchDelay = c_long(sequence.synch_delay)
        SynchPulseWidth = c_long(sequence.synch_pulse_width)
        TriggerInDelay = c_long(sequence.trigger_in_delay)
        ret_val = api.AlpSeqTiming(DeviceId, SequenceId, IlluminateTime, PictureTime, SynchDelay, SynchPulseWidth, TriggerInDelay)
        if ret_val == ALP_OK:
            return
        else:
            raise Exception("AlpSeqTiming: {}".format(ret_val))

    def put(self, sequence): #sequence_id, user_array, pic_offset=ALP_DEFAULT, pic_load=ALP_DEFAULT):
        '''Put sequence'''
        DeviceId = c_ulong(self.id)
        SequenceId = c_ulong(sequence.id)
        PicOffset = c_ulong(sequence.pic_offset)
        PicLoad = c_ulong(sequence.pic_load)
        UserArray = utils.numpy_to_ctypes(sequence.get_user_array(self))
        UserArrayPtr = cast(UserArray, ctypes.c_void_p)
        ret_val = api.AlpSeqPut(DeviceId, SequenceId, PicOffset, PicLoad, UserArrayPtr)
        if ret_val == ALP_OK:
            return
        else:
            raise Exception("AlpSeqPut: {}".format(ret_val))

    def start(self, sequence, infinite_loop=False):
        '''Start sequence'''
        DeviceId = c_ulong(self.id)
        SequenceId = c_ulong(sequence.id)
        if infinite_loop:
            # Launch sequence with an infinite number of loops
            ret_val = api.AlpProjStartCont(DeviceId, SequenceId)
            if ret_val == ALP_OK:
                return
            else:
                raise Exception("AlpProjStartCont: {}".format(ret_val))
        else:
            # Launch sequence with a finite number of loops
            ret_val = api.AlpProjStart(DeviceId, SequenceId)
            if ret_val == ALP_OK:
                return
            else:
                raise Exception("AlpProjStart: {}".format(ret_val))

    def free(self, sequence):
        '''Free sequence'''
        DeviceId = c_ulong(self.id)
        SequenceId = c_ulong(sequence.id)
        ret_val = api.AlpSeqFree(DeviceId, SequenceId)
        if ret_val == ALP_OK:
            return
        else:
            raise Exception("AlpSeqFree: {}".format(ret_val))

    def wait(self, infinite_loop=False):
        '''Wait sequence completion'''
        DeviceId = c_ulong(self.id)
        if infinite_loop:
            _ = input("Press Enter to stop projection...\n")
            DeviceId = c_ulong(self.id)
            ret_val = api.AlpProjHalt(DeviceId)
            if ret_val == ALP_OK:
                return
            else:
                raise Exception("AlpProjHalt: {}".format(ret_val))
        else:
            ret_val = api.AlpProjWait(DeviceId)
            if ret_val == ALP_OK:
                return
            else:
                raise Exception("AlpProjWait: {}".format(ret_val))

    def wait_interruption(self):
        '''Wait sequence interruption'''
        _ = input("Press Enter to stop projection...\n")
        DeviceId = c_ulong(self.id)
        ret_val = api.AlpProjHalt(DeviceId)
        if ret_val == ALP_OK:
            return
        else:
            raise Exception("AlpProjHalt: {}".format(ret_val))

    def invert_projection(self):
        DeviceId = c_ulong(self.id)
        ControlType = c_long(ALP_PROJ_INVERSION)
        ControlValue = c_long(not(ALP_DEFAULT)) # TODO check if correct...
        ret_val = api.AlpProjControl()
        return

    def control_projection(self, mode=None, inversion=None, upside_down=None, wait_until=None, step=None, queue_mode=None, abort_sequence=None, abort_frame=None, reset_queue=None):
        '''TODO add doc...'''
        # TODO mode...
        # Inversion
        if inversion is None:
            pass
        elif inversion is False:
            self._control_projection(ALP_PROJ_INVERSION, ALP_DEFAULT)
        elif inversion is True:
            self._control_projection(ALP_PROJ_INVERSION, not(ALP_DEFAULT))
        else:
            raise ValueError("Unknown mode value {}, should be true or false".format(mode))
        # Upside down
        if upside_down is None:
            pass
        elif upside_down is False:
            self._control_projection(ALP_PROJ_UPSIDE_DOWN, ALP_DEFAULT)
        elif upside_down is True:
            self._control_projection(ALP_PROJ_UPSIDE_DOWN, not(ALP_DEFAULT))
        else:
            raise ValueError("Unknown upside_down value {}, should be true or false".format(upside_down))
        # TODO wait until...
        # TODO step...
        # Queue mode
        if queue_mode is None:
            pass
        elif queue_mode is False:
            self._control_projection(ALP_PROJ_QUEUE_MODE, ALP_PROJ_LEGACY)
        elif queue_mode is True:
            self._control_projection(ALP_PROJ_QUEUE_MODE, ALP_PROJ_SEQUENCE_QUEUE)
        else:
            raise ValueError("Unknown queue_mode value {}, should be true or false".format(queue_mode))
        # TODO abort sequence...
        # TODO abort frame...
        # Reset queue
        if reset_queue is None:
            pass
        elif reset_queue is True:
            self._control_projection(ALP_PROJ_RESET_QUEUE, ALP_DEFAULT)
        elif reset_queue is True:
            self._control_projection(ALP_PROJ_RESET_QUEUE, not(ALP_DEFAULT)) # TODO check if correct...
        else:
            raise ValueError("Unknown reset_queue value {}, should be true or false".format(reset_queue))
        return

    def _control_projection(self, control_type, control_value):
        '''TODO add doc...'''
        DeviceId = c_ulong(self.id)
        ControlType = c_long(control_type)
        ControlValue = c_long(control_value)
        ret_val = api.AlpProjControl(DeviceId, ControlType, ControlValue)
        if ret_val == ALP_OK:
            return
        else:
            raise Exception("AlpProjControl: {}".format(ret_val))

    def inquire_projection(self, inquire_type):
        if type is 'progress':
            DeviceId = c_ulong(self.id)
            InquireType = c_long(ALP_PROJ_PROGRESS)
            UserSruct = tAlpProjProgress()
            UserSructPtr = byref(UserSruct)
            ret_val = api.AlpProjInquireEx(DeviceId, InquireType, UserSructPtr)
            if ret_val == ALP_OK:
                inquire_value = UserSruct.value
                return inquire_value
            else:
                raise Exception("AlpProjInquireEx: {}".format(ret_val))
        else:
            raise ValueError("Unknown inquire_type value {}".format(inquire_type))
