from abc import ABCMeta, abstractmethod


class IStimulus(metaclass=ABCMeta):

    @property
    @abstractmethod
    def control_items(self):

        raise NotImplementedError()

    @property
    @abstractmethod
    def sequences(self):

        raise NotImplementedError()