from abc import ABCMeta, abstractmethod
from typing import Optional, Union

from pyalp.api.low.mock import API as MockAPI
from pyalp.api.low.alp import API as ALPAPI
from pyalp.handler.device import DeviceHandler


class IAPI(metaclass=ABCMeta):

    @abstractmethod
    def handle_device(self, serial_number: Optional[int] = None) -> DeviceHandler:

        raise NotImplementedError()

    @abstractmethod
    def seppuku(self) -> None:

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

    def handle_device(self, serial_number: Optional[int] = None) -> DeviceHandler:

        device_handler = DeviceHandler(serial_number=serial_number, api=self._api)

        return device_handler

    def seppuku(self) -> None:

        self._api.seppuku()

        return
