from typing import Optional

from .. import IAPI
from .adapter import Adapter
from .constant import *


class API(IAPI):

    def __init__(self) -> None:

        self._dll = Adapter()

        return

    def allocate_device(self, device_number: Optional[int] = None) -> int:

        # Prepare arguments.
        if device_number is None:
            device_number_ = MOCK_DEFAULT
        else:
            device_number_ = device_number
        init_flag_ = MOCK_DEFAULT
        # Call function.
        device_id = self._dll.dev_alloc(device_number=device_number_, init_flag=init_flag_)

        return device_id

    def control_device(self, device_id: int, control_type: int, control_value: int) -> None:

        raise NotImplementedError()

    def halt_device(self, device_id: int) -> None:

        raise NotImplementedError()

    def free_device(self, device_id: int) -> None:

        raise NotImplementedError()

    def seppuku(self) -> None:

        self._dll.seppuku()

        return
