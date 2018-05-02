from typing import Optional

from ..api.high import API


class DeviceHandler:
    # TODO add docstring.

    def __init__(self, serial_number: Optional[int], api: API) -> None:
        # TODO add docstring.

        self._serial_number = serial_number
        self._api = api

        self._is_allocated = False
        self._id = None

        return

    def allocate(self):
        # TODO add docstring.

        if not self._is_allocated:
            if self._serial_number is None:
                self._id = self._api.allocate_device()
            else:
                self._id = self._api.allocate_device(device_number=self._serial_number)
            self._is_allocated = True

        return

    def release(self):
        # TODO add docstring.

        if self._is_allocated:
            self._api.halt_device(self._id)
            self._api.free_device(self._id)
            self._api.kill_device(self._id)
            self._is_allocated = False

        return
