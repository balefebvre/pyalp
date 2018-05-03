from abc import ABCMeta, abstractmethod


class ISequence(metaclass=ABCMeta):

    @property
    @abstractmethod
    def size(self):

        raise NotImplementedError()

    @property
    @abstractmethod
    def bit_planes(self):

        raise NotImplementedError()

    @property
    @abstractmethod
    def number_pictures(self):

        raise NotImplementedError()

    @property
    @abstractmethod
    def control_items(self):

        raise NotImplementedError()

    @property
    @abstractmethod
    def data(self):

        raise NotImplementedError()
