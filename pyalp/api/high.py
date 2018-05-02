from abc import ABCMeta, abstractmethod
from typing import Optional, Union

from .low.mock import API as MockAPI
from .low.alp import API as ALPAPI


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

    def halt_device(self, device_id: int) -> None:

        self._api.halt_device(device_id)

        return

    def free_device(self, device_id: int) -> None:

        self._api.free_device(device_id)

        return

    def seppuku(self) -> None:

        self._api.seppuku()

        return
