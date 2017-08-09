import ctypes
from ctypes import c_long, byref, cast
import time

from . import api
from . import utils
# from .base.constant import *
from .base.type import *
from .protocol import Protocol
# from .sequence import Sequence
from .stimulus.base import Stimulus


def allocate(device_number=ALP_DEFAULT, verbose=False):
    """Allocate an ALP hardware system (board set)"""
    device = Device(device_number)
    if verbose:
        device.print_settings()
    return device


class Device(object):
    """TODO add doc...

    TODO complete...
    """

    def __init__(self, device_number):
        """Allocate an ALP hardware system (board set)"""
        # Save input parameter.
        self.nb = device_number
        # Allocate device.
        device_number_ = c_long(device_number)
        init_flag_ = c_long(ALP_DEFAULT)
        device_id_ = c_ulong(ALP_DEFAULT)
        device_id_ptr_ = byref(device_id_)
        ret_val_ = api.AlpDevAlloc(device_number_, init_flag_, device_id_ptr_)
        # Check returned value.
        if ret_val_ == ALP_OK:
            self.id = device_id_.value
        else:
            raise Exception("AlpDevAlloc: {}".format(ret_val_))

    def __del__(self):
        """Deallocate the ALP hardware system (board set)"""
        # Deallocate device.
        device_id_ = c_ulong(self.id)
        ret_val_ = api.AlpDevFree(device_id_)
        # Check returned value.
        if ret_val_ == ALP_OK:
            return
        else:
            raise Exception("AlpDevFree: {}".format(ret_val_))

    def get_id(self):
        """Get DMD identifier"""
        # Return DMD identifier
        return self.id

    def inquire(self, inquire_type):
        """Inquire a parameter setting og the ALP device"""
        device_id_ = c_ulong(self.id)
        inquire_type_ = c_ulong(inquire_type)
        user_var_ = c_ulong(ALP_DEFAULT)
        user_var_ptr_ = byref(user_var_)
        ret_val_ = api.AlpDevInquire(device_id_, inquire_type_, user_var_ptr_)
        if ret_val_ == ALP_OK:
            ret_val_ = user_var_.value
            return ret_val_
        else:
            raise Exception("AlpDevInquire: {}".format(ret_val_))

    def inquire_dmd_type(self, human_readable=False):
        """Inquire DMD type"""
        dmd_type = self.inquire(ALP_DEV_DMDTYPE)
        if human_readable:
            dmd_type = dmd_type_constant_to_string(dmd_type)
        return dmd_type

    def get_resolution(self):
        """Get DMD resolution (in pixels)"""
        # Inquire DMD type
        dmd_type = self.inquire_dmd_type()
        # Retrieve DMD width and height
        # TODO clean following commented lines...
        # if dmd_type in [ALP_DMDTYPE_XGA, ALP_DMDTYPE_XGA_055A, ALP_DMDTYPE_XGA_055X, ALP_DMDTYPE_XGA_07A]:
        if dmd_type in [ALP_DMDTYPE_XGA, ALP_DMDTYPE_XGA_055X, ALP_DMDTYPE_XGA_07A]:
            width = 1024  # px
            height = 768  # px
        # TODO clean following commented lines...
        # elif dmd_type in [ALP_DMDTYPE_SXGA_PLUS]:
        #     width = 1400  # px
        #     height = 1050  # px
        elif dmd_type in [ALP_DMDTYPE_DISCONNECT, ALP_DMDTYPE_1080P_095A]:
            width = 1920  # px
            height = 1080  # px
        elif dmd_type in [ALP_DMDTYPE_WUXGA_096A]:
            width = 1920  # px
            height = 1200  # px
        # TODO clean following commented lines...
        # elif dmd_type in [ALP_DMDTYPE_WQXGA_400MHZ_090A, ALP_DMDTYPE_WQXGA_480MHZ_090A]:
        #     width = 2560 # px
        #     height = 1600 # px
        else:
            dmd_type = self.inquire_dmd_type()
            raise ValueError("Unknown DMD type {}!".format(dmd_type))
        # Save parameters
        resolution = width, height
        # Return DMD resolution
        return resolution

    def inquire_serial_number(self, human_readable=False):
        """Inquire serial number of the ALP device"""
        serial_number = self.inquire(ALP_DEVICE_NUMBER)
        if human_readable:
            serial_number = str(serial_number)
        return serial_number

    def inquire_version(self, human_readable=False):
        """Inquire version number of the ALP device"""
        version = self.inquire(ALP_VERSION)
        if human_readable:
            if version == 0x0401:
                version = "ALP-4.1 [0x0401]"
            else:
                version = "ALP-?.? [{}]".format(hex(version))  # TODO correct.
        return version

    def inquire_available_memory(self, human_readable=False):
        """Inquire available memory of the ALP device"""
        available_memory = self.inquire(ALP_AVAIL_MEMORY)
        if human_readable:
            available_memory = "{} binary frames free".format(available_memory)
        return available_memory

    def inquire_dmd_mode(self, human_readable=False):
        """Inquire DMD mode of the ALP device"""
        dmd_mode = self.inquire(ALP_DEV_DMD_MODE)
        if human_readable:
            if dmd_mode == ALP_DMD_POWER_FLOAT:
                dmd_mode = "ALP_DMD_POWER_FLOAT"
            elif dmd_mode == ALP_DEFAULT:
                dmd_mode = "ALP_DEFAULT"
            else:
                raise NotImplementedError()
        return dmd_mode

    def inquire_display_height(self, human_readable=False):
        """Inquire number of mirror rows on the DMD"""
        display_height = self.inquire(ALP_DEV_DISPLAY_HEIGHT)
        if human_readable:
            display_height = "{} mirror rows on the DMD".format(display_height)
        return display_height

    def inquire_display_width(self, human_readable=False):
        """Inquire number of mirror columns on the DMD"""
        display_width = self.inquire(ALP_DEV_DISPLAY_WIDTH)
        if human_readable:
            display_width = "{} mirror columns on the DMD".format(display_width)
        return display_width

    def inquire_usb_connection(self, human_readable=False):
        """Inquire the status of the USB connection"""
        usb_connection = self.inquire(ALP_USB_CONNECTION)
        if human_readable:
            if usb_connection == ALP_DEFAULT:
                usb_connection = "ALP_DEFAULT"
            elif usb_connection == ALP_DEVICE_REMOVED:
                usb_connection = "ALP_DEVICE_REMOVED"
            else:
                raise NotImplementedError()
        return usb_connection

    # # TODO ALP 4.2 only...
    # def inquire_ddc_fpga_temperature(self):
    #     """Inquire the temperature of the DDC FPGA (IC4)"""
    #     self.ddc_fpga_temperature = self.inquire(ALP_DDC_FPGA_TEMPERATURE)
    #     return self.ddc_fpga_temperature

    # # TODO ALP 4.2 only...
    # def inquire_apps_fpga_temperature(self):
    #     """Inquire the temperature of the Applications FPGA (IC3)"""
    #     self.apps_fpga_temperature = self.inquire(ALP_APPS_FPGA_TEMPERATURE)
    #     return self.apps_fpga_temperature

    # # TODO ALP 4.2 only...
    # def inquire_pcb_temperature(self):
    #     """Inquire the temperature of the sensor IC (IC22)"""
    #     self.pcb_temperature = self.inquire(ALP_PCB_TEMPERATURE)
    #     return self.pcb_temperature

    def inquire_pwm_level(self, human_readable=False):
        """Inquire PWM level (i.e. duty-cycle in percent)"""
        pwm_level = self.inquire(ALP_PWM_LEVEL)
        if human_readable:
            pwm_level = "{} %".format(pwm_level)
        return pwm_level

    def inquire_settings(self, human_readable=False):
        """TODO add docstring"""
        settings = {
            'serial number': self.inquire_serial_number(human_readable=human_readable),
            'version': self.inquire_version(human_readable=human_readable),
            'available memory': self.inquire_available_memory(human_readable=human_readable),
            'dmd type': self.inquire_dmd_type(human_readable=human_readable),
            'dmd mode': self.inquire_dmd_mode(human_readable=human_readable),
            'display height': self.inquire_display_height(human_readable=human_readable),
            'display width': self.inquire_display_width(human_readable=human_readable),
            'usb connection': self.inquire_usb_connection(human_readable=human_readable),
            'pwm level': self.inquire_pwm_level(human_readable=human_readable),
        }
        return settings

    def print_settings(self):
        """TODO add docstring"""

        settings = self.inquire_settings(human_readable=True)

        print("")
        print("------------------ DMD settings ------------------")
        for setting_key, setting_value in settings.items():
            print("{}: {}".format(setting_key, setting_value))
        print("--------------------------------------------------")
        print("")

        return

    def display(self, element):
        """Display element"""
        try:
            if isinstance(element, list):  # TODO create a Queue class...
                queue = element
                for sequence in queue:
                    sequence.display(self)
                    if sequence.is_finite():
                        self.wait_completion()
                    else:
                        self.wait_interruption()
            elif isinstance(element, Protocol):
                element.project(self)
            # elif isinstance(element, Sequence):
            #     sequence = element
            #     sequence.display(self)
            #     self.wait()
            elif isinstance(element, Stimulus):
                element.display(self)
            else:
                raise NotImplementedError("pyalp.device.display")
        except KeyboardInterrupt:
            self.stop()
        return

    def allocate(self, sequence):
        """Allocate sequence"""
        device_id_ = c_ulong(self.id)
        bit_planes_ = c_long(sequence.bit_planes)
        pic_num_ = c_long(sequence.pic_num)
        sequence_id_ = c_ulong(ALP_DEFAULT)
        sequence_id_ptr_ = byref(sequence_id_)
        ret_val_ = api.AlpSeqAlloc(device_id_, bit_planes_, pic_num_, sequence_id_ptr_)
        if ret_val_ == ALP_OK:
            sequence.id = sequence_id_.value
            sequence.device = self
            return
        else:
            raise Exception("AlpSeqAlloc: {}".format(ret_val_))

    def allocate_bis(self, bit_planes, pic_num):
        """Allocate sequence (bis)"""
        device_id_ = c_ulong(self.id)
        bit_planes_ = c_long(bit_planes)
        pic_num_ = c_long(pic_num)
        sequence_id_ = c_ulong(ALP_DEFAULT)
        sequence_id_ptr_ = byref(sequence_id_)
        ret_val_ = api.AlpSeqAlloc(device_id_, bit_planes_, pic_num_, sequence_id_ptr_)
        if ret_val_ == ALP_OK:
            sequence_id = sequence_id_.value
            return sequence_id
        else:
            raise Exception("AlpSeqAlloc: {}".format(ret_val_))

    # def control(self, sequence):
    #     """Control sequence"""
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
        """Control sequence"""
        device_id_ = c_ulong(self.id)
        sequence_id_ = c_ulong(sequence.id)
        control_type_ = c_long(control_type)
        control_value_ = c_long(control_value)
        ret_val_ = api.AlpSeqControl(device_id_, sequence_id_, control_type_, control_value_)
        if ret_val_ == ALP_OK:
            return
        else:
            raise Exception("AlpSeqControl: {}".format(ret_val_))

    def control_repetitions(self, sequence, nb_repetitions):
        """Control sequence repetitions"""
        self.control(sequence, ALP_SEQ_REPEAT, nb_repetitions)
        return

    def control_bit_number(self, sequence, bit_number):
        """Control sequence bit number"""
        self.control(sequence, ALP_BITNUM, bit_number)
        return

    def control_binary_mode(self, sequence, binary_mode):
        """Control sequence binary mode"""
        if binary_mode is 'normal':
            self.control(sequence, ALP_BIN_MODE, ALP_BIN_NORMAL)
        elif binary_mode is 'uninterrupted':
            self.control(sequence, ALP_BIN_MODE, ALP_BIN_UNINTERRUPTED)
        else:
            raise NotImplementedError()

    def control_timing(self, sequence):
        """Set sequence timing"""
        # TODO avoid set timing if possible (i.e. only default values)...
        device_id_ = c_ulong(self.id)
        sequence_id_ = c_ulong(sequence.id)
        illuminate_time_ = c_long(sequence.illuminate_time)
        picture_time_ = c_long(sequence.picture_time)
        synch_delay_ = c_long(sequence.synch_delay)
        synch_pulse_width_ = c_long(sequence.synch_pulse_width)
        trigger_in_delay_ = c_long(sequence.trigger_in_delay)
        ret_val_ = api.AlpSeqTiming(device_id_, sequence_id_, illuminate_time_, picture_time_,
                                    synch_delay_, synch_pulse_width_, trigger_in_delay_)
        if ret_val_ == ALP_OK:
            return
        else:
            raise Exception("AlpSeqTiming: {}".format(ret_val_))

    def put(self, sequence):  # sequence_id, user_array, pic_offset=ALP_DEFAULT, pic_load=ALP_DEFAULT):
        """Put sequence"""
        device_id_ = c_ulong(self.id)
        sequence_id_ = c_ulong(sequence.id)
        pic_offset_ = c_ulong(sequence.pic_offset)
        pic_load_ = c_ulong(sequence.pic_load)
        user_array_ = utils.numpy_to_ctypes(sequence.get_user_array())
        user_array_ptr_ = cast(user_array_, ctypes.c_void_p)
        ret_val_ = api.AlpSeqPut(device_id_, sequence_id_, pic_offset_, pic_load_, user_array_ptr_)
        if ret_val_ == ALP_OK:
            return
        else:
            raise Exception("AlpSeqPut: {}".format(ret_val_))

    def start(self, sequence, infinite_loop=False):
        """Start sequence"""

        device_id_ = c_ulong(self.id)
        sequence_id_ = c_ulong(sequence.id)

        if infinite_loop:
            # Launch sequence with an infinite number of loops
            ret_val_ = api.AlpProjStartCont(device_id_, sequence_id_)
            if ret_val_ == ALP_OK:
                return
            else:
                raise Exception("AlpProjStartCont: {}".format(ret_val_))
        else:
            # Launch sequence with a finite number of loops
            ret_val_ = api.AlpProjStart(device_id_, sequence_id_)
            if ret_val_ == ALP_OK:
                return
            else:
                raise Exception("AlpProjStart: {}".format(ret_val_))

    def free(self, sequence):
        """Free sequence"""
        device_id_ = c_ulong(self.id)
        sequence_id = c_ulong(sequence.id)
        ret_val_ = api.AlpSeqFree(device_id_, sequence_id)
        if ret_val_ == ALP_OK:
            return
        else:
            raise Exception("AlpSeqFree: {}".format(ret_val_))

    def wait(self, infinite_loop=False, active=True):
        """Wait sequence completion.

        Parameters
        ----------
        infinite_loop: boolean, optional
            The default value is False.
        active: boolean, optional
            Waiting mode: active or passive. Keyboard interruption is allowed under active mode only. The default value
            is True.
        """
        device_id_ = c_ulong(self.id)
        if infinite_loop:
            _ = input("Press Enter to stop projection...\n")
            device_id_ = c_ulong(self.id)
            ret_val_ = api.AlpProjHalt(device_id_)
            if ret_val_ == ALP_OK:
                return
            else:
                raise Exception("AlpProjHalt: {}".format(ret_val_))
        else:
            if active:
                projection_progress = self.inquire_projection('progress')
                while not projection_progress.is_idle:
                    time.sleep(30.0e-3)
                    projection_progress = self.inquire_projection('progress')
            else:
                ret_val_ = api.AlpProjWait(device_id_)
                if ret_val_ == ALP_OK:
                    return
                else:
                    raise Exception("AlpProjWait: {}".format(ret_val_))

    def wait_completion(self):
        """TODO add docstring."""

        raise NotImplementedError()

    def wait_interruption(self):
        """Wait sequence interruption"""
        _ = input("Press Enter to stop projection...\n")
        device_id_ = c_ulong(self.id)
        ret_val_ = api.AlpProjHalt(device_id_)
        if ret_val_ == ALP_OK:
            return
        else:
            raise Exception("AlpProjHalt: {}".format(ret_val_))

    def stop(self):
        """Stop running sequence display."""

        device_id_ = c_long(self.id)
        ret_val_ = api.AlpProjHalt(device_id_)
        if ret_val_ == ALP_OK:
            return
        else:
            raise Exception("AlpProjHalt: {}".format(ret_val_))

    @staticmethod
    def invert_projection():
        # DeviceId = c_ulong(self.id)
        # ControlType = c_long(ALP_PROJ_INVERSION)
        # ControlValue = c_long(not(ALP_DEFAULT))  # TODO check if correct...
        ret_val_ = api.AlpProjControl()
        if ret_val_ == ALP_OK:
            return
        else:
            raise Exception("AlpProjControl: {}".format(ret_val_))

    def control_projection(self, mode=None, inversion=None, upside_down=None, wait_until=None, step=None,
                           queue_mode=None, abort_sequence=None, abort_frame=None, reset_queue=None):
        """TODO add doc..."""
        # TODO mode...
        # Inversion
        if inversion is None:
            pass
        elif inversion is False:
            self._control_projection(ALP_PROJ_INVERSION, ALP_DEFAULT)
        elif inversion is True:
            self._control_projection(ALP_PROJ_INVERSION, not ALP_DEFAULT)
        else:
            raise ValueError("Unknown mode value {}, should be true or false".format(mode))
        # Upside down
        if upside_down is None:
            pass
        elif upside_down is False:
            self._control_projection(ALP_PROJ_UPSIDE_DOWN, ALP_DEFAULT)
        elif upside_down is True:
            self._control_projection(ALP_PROJ_UPSIDE_DOWN, not ALP_DEFAULT)
        else:
            raise ValueError("Unknown upside_down value {}, should be true or false".format(upside_down))
        if wait_until is None:
            pass
        else:
            raise NotImplementedError()
            # TODO complete.
        if step is None:
            pass
        else:
            raise NotImplementedError()
            # TODO complete.
        # Queue mode
        if queue_mode is None:
            pass
        elif queue_mode is False:
            self._control_projection(ALP_PROJ_QUEUE_MODE, ALP_PROJ_LEGACY)
        elif queue_mode is True:
            self._control_projection(ALP_PROJ_QUEUE_MODE, ALP_PROJ_SEQUENCE_QUEUE)
        else:
            raise ValueError("Unknown queue_mode value {}, should be true or false".format(queue_mode))
        if abort_sequence is None:
            pass
        else:
            raise NotImplementedError()
            # TODO complete.
        if abort_frame is None:
            pass
        else:
            raise NotImplementedError()
            # TODO complete.
        # Reset queue
        if reset_queue is None:
            pass
        elif reset_queue is True:
            self._control_projection(ALP_PROJ_RESET_QUEUE, ALP_DEFAULT)
        elif reset_queue is True:
            self._control_projection(ALP_PROJ_RESET_QUEUE, not ALP_DEFAULT)  # TODO check if correct...
        else:
            raise ValueError("Unknown reset_queue value {}, should be true or false".format(reset_queue))
        return

    def _control_projection(self, control_type, control_value):
        """TODO add doc..."""
        device_id_ = c_ulong(self.id)
        control_type_ = c_long(control_type)
        control_value_ = c_long(control_value)
        ret_val_ = api.AlpProjControl(device_id_, control_type_, control_value_)
        if ret_val_ == ALP_OK:
            return
        else:
            raise Exception("AlpProjControl: {}".format(ret_val_))

    def inquire_projection(self, inquire_type):
        """Inquire information about general ALP setting for the sequence display.

        Parameters
        ----------
        inquire_type: str
            If equal to 'progress' then retrieve information about active sequences and the sequence queue.

        """
        if inquire_type is 'progress':
            device_id_ = c_ulong(self.id)
            inquire_type_ = c_long(ALP_PROJ_PROGRESS)
            user_struct_ = tAlpProjProgress()
            user_struct_ptr_ = byref(user_struct_)
            ret_val_ = api.AlpProjInquireEx(device_id_, inquire_type_, user_struct_ptr_)
            if ret_val_ == ALP_OK:
                inquire_value = user_struct_
                return inquire_value
            else:
                raise Exception("AlpProjInquireEx: {}".format(ret_val_))
        else:
            raise ValueError("Unknown inquire_type value {}".format(inquire_type))

    def synchronize(self, sleep_duration=30.0e-3):
        """TODO add docstring

        More sophisticated synchronization method by supervision of sequence progress.

        Parameter
        ---------
        sleep_duration: float
            Sleep duration [s]. The default value is 30.0e-3.

        """

        projection_progress = self.inquire_projection('progress')
        while projection_progress.nWaitingSequences >= 1 or projection_progress.SequenceId == 0:
            projection_progress = self.inquire_projection('progress')
            time.sleep(sleep_duration)

        return
