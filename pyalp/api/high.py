from abc import ABCMeta, abstractmethod
from numpy import ndarray
from typing import Optional, Union

from .low.mock import API as MockAPI
from .low.alp import API as ALPAPI
from .low.constant import *


class IAPI(metaclass=ABCMeta):

    @abstractmethod
    def allocate_device(self, device_number: int = 0) -> int:

        raise NotImplementedError()


class API(IAPI):

    def __init__(self, api: Union[MockAPI, ALPAPI]) -> None:
        """Initialize the high-level API.

        Argument:
            api: Union[pyalp.api.low.alp.API, pyalp.api.low.mock.API]
                The low-level API.
        """

        self._api = api

        return

    def allocate_device(self, device_number: Optional[int] = None) -> int:

        if device_number is None:
            device_id = self._api.allocate_device()
        else:
            device_id = self._api.allocate_device(device_number=device_number)

        return device_id

    def inquire_device_height(self, device_id: int) -> int:

        device_height = self._api.inquire_device(device_id, DEV_DISPLAY_HEIGHT)

        return device_height

    def inquire_device_width(self, device_id: int) -> int:

        device_width = self._api.inquire_device(device_id, DEV_DISPLAY_WIDTH)

        return device_width

    def halt_device(self, device_id: int) -> None:

        self._api.halt_device(device_id)

        return

    def free_device(self, device_id: int) -> None:

        self._api.free_device(device_id)

        return

    def allocate_sequence(self, device_id: int, bit_planes: int, number_pictures: int) -> int:

        sequence_id = self._api.allocate_sequence(device_id, bit_planes, number_pictures)

        return sequence_id

    def put_sequence(self, device_id: int, sequence_id: int, picture_offset: int, number_pictures: int, data: ndarray) -> None:

        self._api.put_sequence(device_id, sequence_id, picture_offset, number_pictures, data)

        return

    def free_sequence(self, device_id: int, sequence_id: int) -> None:

        self._api.free_sequence(device_id, sequence_id)

        return

    def seppuku(self) -> None:

        self._api.seppuku()

        return
