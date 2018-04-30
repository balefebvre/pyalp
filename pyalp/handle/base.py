from abc import ABCMeta, abstractmethod


def handle(mock=False, device_number=0):
    """Instantiate a handle on a device.

    Arguments:
        mock: boolean (optional)
            Specifies if a mock device should be used.
            The default value is False.
        device_number: integer (optional)
            Specifies the device to be used (i.e. serial number).
            The default value is 0.
    """

    if mock:
        from .matplotlib import MatplotlibHandle
        handle_ = MatplotlibHandle(device_number=device_number)
    else:
        from .alp import ALPHandle
        handle_ = ALPHandle(device_number=device_number)

    return handle_


class Handle(metaclass=ABCMeta):
    """Handle interface."""

    @abstractmethod
    def __init__(self):
        """Initialize a handle."""

        pass

    @abstractmethod
    def release(self):
        """Release the handle."""

        raise NotImplementedError()
