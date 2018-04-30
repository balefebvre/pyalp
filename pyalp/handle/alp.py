import numpy as np

from .base import Handle as BaseHandle
from ..device_bis.alp import Device


class Handle(BaseHandle):
    """ALP handle"""

    def __init__(self, device_number=0):
        """Initialize an ALP handle.

        Argument:
            device_number: integer (optional)
                Specifies the device to be used (i.e. serial number).
                The default value is 0.
        """

        super().__init__()

        self._device = Device()
        self._device.allocate(device_number=device_number)

        self._is_active = True

        return

    def release(self):
        """Release Matplotlib handle."""

        if self._is_active:
            self._device.halt()
            self._device.free()
            self._is_active = False

        return

    def display_rectangle(self):
        # Display a rectangle.

        # Allocate sequence.
        bit_planes = 1
        number_pictures = 100  # TODO correct.
        sequence_id = self._device.allocate_sequence(bit_planes, number_pictures)

        # Put sequence.
        pic_offset = 0
        pic_load = number_pictures
        width = 1920  # TODO compute it from DMD type.
        height = 1080  # TODO compute it from DMD type.
        shape = (number_pictures, height, width)
        dtype = np.uint8
        user_array = np.zeros(shape, dtype=dtype)
        i_min = 500  # TODO compute it
        i_max = 1500  # TODO compute it.
        j_min = 250  # TODO compute it.
        j_max = 750  # TODO compute it.
        user_array[:, j_min:j_max, i_min:i_max] = np.iinfo(dtype).max
        self._device.put_sequence(sequence_id, pic_offset, pic_load, user_array)

        # Start projection.
        self._device.start_projection(sequence_id)

        # Wait for the completion of the projection.
        self._device.wait_projection()

        # Free sequence.
        self._device.free_sequence(sequence_id)

        return
