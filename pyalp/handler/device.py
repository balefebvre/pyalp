from typing import Optional

from ..api.high import API


class DeviceHandler:

    def __init__(self, serial_number: Optional[int], api: API) -> None:

        self._serial_number = serial_number
        self._api = api

        self._is_allocated = False
        self._id = None

        return

    def allocate(self) -> None:

        if not self._is_allocated:
            if self._serial_number is None:
                self._id = self._api.allocate_device()
            else:
                self._id = self._api.allocate_device(device_number=self._serial_number)
            self._is_allocated = True

        return

    def release(self) -> None:

        if self._is_allocated:
            self._api.halt_device(self._id)
            self._api.free_device(self._id)
            self._is_allocated = False

        return

    def show_info(self) -> None:

        print("Show info...")

        # TODO complete.

        return

    def display_rectangle(self) -> None:

        print("Display rectangle...")

        # TODO inquire height and width.
        height = self._api.inquire_device_height(self._id)
        width = self._api.inquire_device_width(self._id)
        print("height, width: {}, {}".format(height, width))
        # TODO allocate sequence.
        bit_planes = 8
        number_pictures = 10
        sequence_id = self._api.allocate_sequence(self._id, bit_planes, number_pictures)
        print("sequence_id: {}".format(sequence_id))
        # TODO complete.

        return

    def display_checkerboard(self) -> None:

        print("Display checkerboard...")

        # TODO complete.

        return

    def display_film(self) -> None:

        print("Display film...")

        # TODO complete.

        return
