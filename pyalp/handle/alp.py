from .base import Handle
from ..device_bis import ALPDevice


class ALPHandle(Handle):
    """ALPHandle"""

    def __init__(self, device_number=0):
        """Initialize an ALP handle.

        Argument:
            device_number: integer (optional)
                Specifies the device to be used (i.e. serial number).
                The default value is 0.
        """

        super().__init__()

        self._device = ALPDevice()
        # self._device.turn_on()  # TODO remove line.
        self._device.allocate(device_number)

        self._is_active = True

        return

    def release(self):
        """Release Matplotlib handle."""

        if self._is_active:
            self._device.halt()  # TODO execute line if necessary only.
            self._device.free()
            # self._device.turn_off()  # TODO remove line.
            self._is_active = False
        else:
            pass  # TODO raise warning.

        return
