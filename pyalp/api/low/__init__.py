from abc import ABCMeta, abstractmethod
from numpy import ndarray
from typing import Optional


class IAPI(metaclass=ABCMeta):

    @abstractmethod
    def allocate_device(self, device_number: Optional[int] = None) -> int:

        raise NotImplementedError()

    @abstractmethod
    def control_device(self, device_id: int, control_type: int, control_value: int) -> None:

        raise NotImplementedError()

    @abstractmethod
    def halt_device(self, device_id: int) -> None:

        raise NotImplementedError()

    @abstractmethod
    def free_device(self, device_id: int) -> None:

        raise NotImplementedError()

    @abstractmethod
    def allocate_sequence(self, device_id: int, bit_planes: int, number_pictures: int) -> int:

        raise NotImplementedError()

    @abstractmethod
    def put_sequence(self, device_id: int, sequence_id: int, picture_offset: int, number_pictures: int, data: ndarray) -> None:

        raise NotImplementedError()

    @abstractmethod
    def free_sequence(self, device_id: int, sequence_id: int) -> None:

        raise NotImplementedError()

    @abstractmethod
    def seppuku(self) -> None:

        raise NotImplementedError()

    # TODO add missing methods.
