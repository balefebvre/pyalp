from numpy import ndarray
from typing import Optional

from .. import IAPI
from ..constant import *
from .adapter import Adapter
from .constant import *


class API(IAPI):

    def __init__(self, dll) -> None:

        self._dll = Adapter(dll)

        return

    def allocate_device(self, device_number: Optional[int] = None) -> int:
        # TODO add docstring.

        # Prepare arguments.
        if device_number is None:
            device_number_ = ALP_DEFAULT
        else:
            device_number_ = device_number
        init_flag_ = ALP_DEFAULT
        # Call function.
        device_id = self._dll.dev_alloc(device_number_, init_flag_)

        return device_id

    control_type_map = {
        SYNCH_POLARITY: ALP_SYNCH_POLARITY,
        TRIGGER_EDGE: ALP_TRIGGER_EDGE,
        DEV_DMDTYPE: ALP_DEV_DMDTYPE,
        DEV_DMD_MODE: ALP_DEV_DMD_MODE,
        USB_CONNECTION: ALP_USB_CONNECTION,
        PWM_LEVEL: ALP_PWM_LEVEL,
    }

    control_value_map = {
        DEFAULT: ALP_DEFAULT,
        LEVEL_HIGH: ALP_LEVEL_HIGH,
        LEVEL_LOW: ALP_LEVEL_LOW,
        EDGE_FALLING: ALP_EDGE_FALLING,
        EDGE_RISING: ALP_EDGE_RISING,
        DMDTYPE_XGA_07A: ALP_DMDTYPE_XGA_07A,
        DMDTYPE_XGA_055X: ALP_DMDTYPE_XGA_055X,
        DMDTYPE_1080P_095A: ALP_DMDTYPE_1080P_095A,
        DMDTYPE_WUXGA_096A: ALP_DMDTYPE_WUXGA_096A,
        DMD_POWER_FLOAT: ALP_DMD_POWER_FLOAT,
    }

    def control_device(self, device_id: int, control_type: int, control_value: int) -> None:
        # TODO add docstring.

        # Prepare arguments.
        if control_type in self.control_type_map:
            control_type_ = self.control_type_map[control_type]
        else:
            string = "invalid argument 'control_type': {}"
            message = string.format(control_type)
            raise ValueError(message)
        if control_type != PWM_LEVEL:
            if control_value in self.control_value_map:
                control_value_ = self.control_value_map[control_value]
            else:
                string = "invalid argument 'control_value': {}"
                message = string.format(control_value)
                raise ValueError(message)
        else:
            control_value_ = control_value
        # Call function.
        self._dll.dev_control(device_id, control_type_, control_value_)

        return

    inquire_type_map = {
        DEVICE_NUMBER: ALP_DEVICE_NUMBER,
        VERSION: ALP_VERSION,
        AVAIL_MEMORY: ALP_AVAIL_MEMORY,
        SYNCH_POLARITY: ALP_SYNCH_POLARITY,
        TRIGGER_EDGE: ALP_TRIGGER_EDGE,
        DEV_DMDTYPE: ALP_DEV_DMDTYPE,
        DEV_DMD_MODE: ALP_DEV_DMD_MODE,
        DEV_DISPLAY_HEIGHT: ALP_DEV_DISPLAY_HEIGHT,
        DEV_DISPLAY_WIDTH: ALP_DEV_DISPLAY_WIDTH,
        USB_CONNECTION: ALP_USB_CONNECTION,
        # DDC_FPGA_TEMPERATURE: ALP_DDC_FPGA_TEMPERATURE,  # TODO remove (ALP-4.2 only).
        # APPS_FPGA_TEMPERATURE: ALP_APPS_FPGA_TEMPERATURE,  # TODO remove (ALP-4.2 only).
        # PCB_TEMPERATURE: ALP_PCB_TEMPERATURE,  # TODO remove (ALP-4.2 only).
        PWM_LEVEL: ALP_PWM_LEVEL,
    }

    inquire_value_map = {
        ALP_DEFAULT: DEFAULT,
        ALP_LEVEL_HIGH: LEVEL_HIGH,
        ALP_LEVEL_LOW: LEVEL_LOW,
        ALP_EDGE_FALLING: EDGE_FALLING,
        ALP_EDGE_RISING: EDGE_RISING,
        ALP_DMDTYPE_XGA_07A: DMDTYPE_XGA_07A,
        ALP_DMDTYPE_XGA_055X: DMDTYPE_XGA_055X,
        ALP_DMDTYPE_1080P_095A: DMDTYPE_1080P_095A,
        ALP_DMDTYPE_WUXGA_096A: DMDTYPE_WUXGA_096A,
        ALP_DMDTYPE_DISCONNECT: DMDTYPE_DISCONNECT,
        ALP_DMD_POWER_FLOAT: DMD_POWER_FLOAT,
        ALP_DEVICE_REMOVED: DEVICE_REMOVED,
    }

    def inquire_device(self, device_id: int, inquire_type: int) -> int:
        # TODO add docstring.

        # Prepare arguments.
        if inquire_type in self.inquire_type_map:
            inquire_type_ = self.inquire_type_map[inquire_type]
        else:
            string = "invalid argument 'inquire_type': {}"
            message = string.format(inquire_type)
            raise ValueError(message)
        # Call function.
        inquire_value_ = self._dll.dev_inquire(device_id, inquire_type_)
        # Prepare result.
        if inquire_type not in [DEVICE_NUMBER, VERSION, AVAIL_MEMORY, DEV_DISPLAY_HEIGHT, DEV_DISPLAY_WIDTH, PWM_LEVEL]:
            if inquire_value_ in self.inquire_value_map:
                inquire_value = self.inquire_value_map[inquire_value_]
            else:
                string = "invalid result 'inquire_value': {}"
                message = string.format(inquire_value_)
                raise ValueError(message)
        else:
            inquire_value = inquire_value_

        return inquire_value

    control_type_extended_map = {
        DEV_DYN_SYNCH_OUT1_GATE: ALP_DEV_DYN_SYNCH_OUT1_GATE,
        DEV_DYN_SYNCH_OUT2_GATE: ALP_DEV_DYN_SYNCH_OUT2_GATE,
        DEV_DYN_SYNCH_OUT3_GATE: ALP_DEV_DYN_SYNCH_OUT3_GATE,
    }

    def control_device_extended(self, device_id: int, control_type: int, user_struct: ndarray) -> None:
        # TODO add docstring.

        # Prepare arguments.
        if control_type in self.control_type_extended_map:
            control_type_ = self.control_type_extended_map[control_type]
        else:
            string = "invalid argument 'control_type': {}"
            message = string.format(control_type)
            raise ValueError(message)
        # Call function.
        self._dll.dev_control_ex(device_id, control_type_, user_struct)

        return

    def halt_device(self, device_id: int) -> None:
        # TODO add docstring.

        # Call function.
        self._dll.dev_halt(device_id)

        return

    def free_device(self, device_id: int) -> None:
        # TODO add docstring.

        # Call function.
        self._dll.dev_free(device_id)

        return

    def seppuku(self) -> None:

        # Call function.
        self._dll.seppuku()

        return
