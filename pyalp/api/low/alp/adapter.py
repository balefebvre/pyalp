from ctypes import byref, c_long, c_ulong
from numpy import ndarray

from ..error import *
from .constant import *
from .utils import c_ubyte_array


class Adapter:

    def __init__(self, dll):

        self._dll = dll

        return

    def dev_alloc(self, device_number: int, init_flag: int) -> int:
        """Allocate an ALP hardware system.

        Arguments:
            device_number: Optional[int]
                Specifies the device to be used.
            init_flag: Optional[int]
                Specifies the type of initialization to perform on the device.
        Return:
            device_id: int
                The ALP device identifier.
        """

        # Prepare arguments.
        device_number_ = c_long(device_number)
        init_flag_ = c_long(init_flag)
        device_id_ = c_ulong(ALP_DEFAULT)
        # Call function.
        ret_val = self._dll.AlpDevAlloc(device_number_, init_flag_, byref(device_id_))
        # Handle error (if necessary).
        if ret_val == ALP_OK:
            pass
        elif ret_val == ALP_ADDR_INVALID:
            raise AddrInvalidError()
        elif ret_val == ALP_NOT_ONLINE:
            raise NotOnlineError()
        elif ret_val == ALP_NOT_READY:
            raise NotReadyError()
        elif ret_val == ALP_ERROR_INIT:
            raise InitError()
        elif ret_val == ALP_LOADER_VERSION:
            raise LoaderVersionError()
        elif ret_val == ALP_ERROR_COMM:
            raise CommError()
        elif ret_val == ALP_DEVICE_REMOVED:
            raise DeviceRemovedError()
        else:
            raise NotImplementedError(ret_val)
        # Prepare result.
        device_id = device_id_.value

        return device_id

    def dev_control(self, device_id: int, control_type: int, control_value: int) -> None:
        """Change the display properties of the ALP.

        Arguments:
            device_id: int
                ALP device identifier.
            control_type: int
                ALP device parameter setting to modify.
            control_value: int
                Value of the modified ALP device parameter setting.
        """

        # Prepare arguments.
        device_id_ = c_ulong(device_id)
        control_type_ = c_long(control_type)
        control_value_ = c_long(control_value)
        # Call function.
        ret_val = self._dll.AlpDevControl(device_id_, control_type_, control_value_)
        # Handle error (if necessary).
        if ret_val == ALP_OK:
            pass
        elif ret_val == ALP_NOT_AVAILABLE:
            raise NotAvailableError()
        elif ret_val == ALP_NOT_READY:
            raise NotReadyError()
        elif ret_val == ALP_NOT_IDLE:
            raise NotIdleError()
        elif ret_val == ALP_PARM_INVALID:
            raise ParmInvalidError()
        elif ret_val == ALP_NOT_ONLINE:
            raise NotOnlineError()
        elif ret_val == ALP_NOT_CONFIGURED:
            raise NotConfiguredError()
        elif ret_val == ALP_ERROR_POWER_DOWN:
            raise PowerDownError()
        else:
            raise NotImplementedError(ret_val)

        return

    def dev_inquire(self, device_id: int, inquire_type: int) -> int:
        """Inquire a parameter setting of the specified ALP device.

        Arguments:
            device_id: int
                ALP device identifier.
            inquire_type: int
                ALP device parameter setting to inquire.
        Return:
            inquire_value: int
                Value of the requested ALP device parameter setting.
        """

        # Prepare arguments.
        device_id_ = c_ulong(device_id)
        inquire_type_ = c_long(inquire_type)
        user_var_ = c_long(ALP_DEFAULT)
        # Call function.
        ret_val = self._dll.AlpDevInquire(device_id_, inquire_type_, byref(user_var_))
        # Handle error (if necessary).
        if ret_val == ALP_OK:
            pass
        elif ret_val == ALP_NOT_AVAILABLE:
            raise NotAvailableError()
        elif ret_val == ALP_PARM_INVALID:
            raise ParmInvalidError()
        elif ret_val == ALP_ADDR_INVALID:
            raise AddrInvalidError()
        elif ret_val == ALP_DEVICE_REMOVED:
            raise DeviceRemovedError()
        else:
            raise NotImplementedError(ret_val)
        # Prepare result.
        inquire_value = user_var_.value

        return inquire_value

    def dev_control_ex(self, device_id: int, control_type: int, user_struct: ndarray) -> None:
        """Change the display properties of the ALP (extended).

        Arguments:
            device_id: int
                ALP device identifier.
            control_type: int
                ALP device parameter setting to modify.
            user_struct
                Value of the modified ALP device parameter setting.
        """

        # # Prepare arguments.
        # device_id_ = c_ulong(device_id)
        # control_type_ = c_long(control_type)
        # user_struct_ = None  # TODO correct.
        # # Call function.
        # ret_val = self._dll.AlpDevControl(device_id_, control_type_, byref(user_struct_))
        # # Handle error (if necessary).
        # if ret_val == ALP_OK:
        #     pass
        # elif ret_val == ALP_NOT_AVAILABLE:
        #     raise NotAvailableError()
        # elif ret_val == ALP_NOT_READY:
        #     raise NotReadyError()
        # elif ret_val == ALP_PARM_INVALID:
        #     raise ParmInvalidError()
        # else:
        #     raise NotImplementedError(ret_val)
        #
        # return

        raise NotImplementedError()

    def dev_halt(self, device_id):
        """Put the ALP in an idle wait state.

        Argument:
            device_id: int
                ALP identifier of the device to be freed.
        """

        # Prepare arguments.
        device_id_ = c_ulong(device_id)
        # Call function.
        ret_val = self._dll.AlpDevHalt(device_id_)
        # Handle error (if necessary).
        if ret_val == ALP_OK:
            pass
        elif ret_val == ALP_NOT_AVAILABLE:
            raise NotAvailableError()
        else:
            raise NotImplementedError(ret_val)

        return

    def dev_free(self, device_id: int) -> None:
        """De-allocate a previously allocated ALP device.

        Argument:
            device_id: int
                ALP identifier of the device to be freed.
        """

        # Prepare arguments.
        device_id_ = c_ulong(device_id)
        # Call function.
        ret_val = self._dll.AlpDevFree(device_id_)
        # Handle error (if necessary).
        if ret_val == ALP_OK:
            pass
        elif ret_val == ALP_NOT_AVAILABLE:
            raise NotAvailableError()
        elif ret_val == ALP_NOT_READY:
            raise NotReadyError()
        elif ret_val == ALP_NOT_IDLE:
            raise NotIdleError()
        else:
            raise NotImplementedError(ret_val)

        return

    def seq_alloc(self, device_id, bit_planes, pic_num):

        # Prepare arguments.
        device_id_ = c_ulong(device_id)
        bit_planes_ = c_long(bit_planes)
        pic_num_ = c_ulong(pic_num)
        sequence_id_ = c_ulong(ALP_DEFAULT)
        # Call function.
        ret_val = self._dll.AlpSeqAlloc(device_id_, bit_planes_, pic_num_, byref(sequence_id_))
        # Handle error (if necessary).
        if ret_val == ALP_OK:
            pass
        elif ret_val == ALP_NOT_AVAILABLE:
            raise NotAvailableError()
        elif ret_val == ALP_NOT_READY:
            raise NotReadyError()
        elif ret_val == ALP_PARM_INVALID:
            raise ParmInvalidError()
        elif ret_val == ALP_ADDR_INVALID:
            raise AddrInvalidError()
        elif ret_val == ALP_MEMORY_FULL:
            raise MemoryFullError()
        else:
            raise NotImplementedError(ret_val)
        # Prepare result.
        sequence_id = sequence_id_.value

        return sequence_id

    def seq_control(self, device_id, sequence_id, control_type, control_value):

        raise NotImplementedError()

    def seq_timing(self, device_id, sequence_id, illuminate_time, picture_time,
                   synch_delay, synch_pulse_width, trigger_in_delay):

        raise NotImplementedError()

    def seq_inquire(self, device_id, sequence_id, inquire_type):

        raise NotImplementedError()

    def seq_put(self, device_id, sequence_id, pic_offset, pic_load, user_array):

        # Prepare arguments.
        device_id_ = c_ulong(device_id)
        sequence_id_ = c_ulong(sequence_id)
        pic_offset_ = c_long(pic_offset)
        pic_load_ = c_long(pic_load)
        user_array_ = c_ubyte_array(user_array)
        # Call function.
        ret_val = self._dll.AlpSeqPut(device_id_, sequence_id_, pic_offset_, pic_load_, user_array_)
        # Handle error (if necessary).
        if ret_val == ALP_OK:
            pass
        elif ret_val == ALP_NOT_AVAILABLE:
            raise NotAvailableError()
        elif ret_val == ALP_NOT_READY:
            raise NotReadyError()
        elif ret_val == ALP_PARM_INVALID:
            raise ParmInvalidError()
        elif ret_val == ALP_ERROR_COMM:
            raise CommError()
        elif ret_val == ALP_SEQ_IN_USE:
            raise SeqInUseError()
        elif ret_val == ALP_HALTED:
            raise HaltedError()
        elif ret_val == ALP_ADDR_INVALID:
            raise AddrInvalidError()
        else:
            raise NotImplementedError(ret_val)

        return

    def seq_free(self, device_id, sequence_id):

        # Prepare arguments.
        device_id_ = c_ulong(device_id)
        sequence_id_ = c_ulong(sequence_id)
        # Call function.
        ret_val = self._dll.AlpSeqFree(device_id_, sequence_id_)
        # Handle error (if necessary).
        if ret_val == ALP_OK:
            pass
        elif ret_val == ALP_NOT_AVAILABLE:
            raise NotAvailableError()
        elif ret_val == ALP_NOT_READY:
            raise NotReadyError()
        elif ret_val == ALP_NOT_READY:
            raise NotIdleError()
        elif ALP_SEQ_IN_USE:
            raise SeqInUseError()
        elif ALP_PARM_INVALID:
            raise ParmInvalidError()
        else:
            raise NotImplementedError(ret_val)

        return

    def proj_control(self, device_id, control_type, control_value):

        raise NotImplementedError()

    def proj_inquire(self, device_id, inquire_type):

        raise NotImplementedError()

    # def proj_control_ex(self, device_id, control_type, user_struct):
    #
    #     raise NotImplementedError()

    # def proj_inquire_ex(self, device_id, inquire_type):
    #
    #     raise NotImplementedError()

    def proj_start(self, device_id, sequence_id):

        raise NotImplementedError()

    def proj_start_cont(self, device_id, sequence_id):

        raise NotImplementedError()

    def proj_halt(self, device_id):

        raise NotImplementedError()

    def proj_wait(self, device_id):

        raise NotImplementedError()

    def led_alloc(self, device_id, led_type, user_var):

        raise NotImplementedError()

    def led_free(self, device_id, led_id):

        raise NotImplementedError()

    def led_control(self, device_id, led_id, control_type, control_value):

        raise NotImplementedError()

    def led_inquire(self, device_id, led_id, inquire_type):

        raise NotImplementedError()

    # def led_control_ex(self, device_id, led_id, control_type, user_struct):
    #
    #     raise NotImplementedError()

    # def led_inquire_ex(self, device_id, led_id, inquire_type):
    #
    #     raise NotImplementedError()

    def seppuku(self):

        pass

        return
