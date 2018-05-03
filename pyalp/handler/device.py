from collections import deque
from typing import Optional, Union

from pyalp.api.low.alp import API as ALPAPI
from pyalp.api.low.alp import API as MockAPI
from pyalp.api.low.constant import *
from pyalp.stimulus_bis import IStimulus
from pyalp.stimulus_bis.white_frame import WhiteFrameStimulus


class DeviceHandler:

    def __init__(self, serial_number: Optional[int], api: Union[ALPAPI, MockAPI]) -> None:

        self._serial_number = serial_number
        self._api = api

        self._is_allocated = False
        self._id = None

        return

    @property
    def height(self):

        return self._api.inquire_device(self._id, DEV_DISPLAY_HEIGHT)

    @property
    def width(self):

        return self._api.inquire_device(self._id, DEV_DISPLAY_WIDTH)

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

    # def show_info(self) -> None:
    #
    #     print("Show info...")
    #
    #     # TODO complete.
    #
    #     return

    def display(self, stimulus: IStimulus) -> None:

        allocated_sequences = {}
        allocated_sequence_counters = {}
        history = deque()

        # Control device.
        for control_type, control_value in stimulus.control_items:
            self._api.control_device(self._id, control_type, control_value)

        try:

            # Project stimulus.
            for sequence in stimulus.sequences:

                if sequence in allocated_sequences:

                    # Update internal variables.
                    sequence_id = allocated_sequences[sequence]
                    allocated_sequence_counters[sequence] += 1
                    history.append(sequence)

                else:

                    # Check available memory.
                    available_memory = self._api.inquire_device(self._id, AVAIL_MEMORY)
                    while available_memory < sequence.size and len(allocated_sequences) > 1:
                        # Find oldest allocated sequence.
                        old_sequence = history.popleft()
                        while allocated_sequence_counters[old_sequence] > 1:
                            allocated_sequence_counters[old_sequence] -= 1
                            old_sequence = history.popleft()
                        # Free sequence.
                        self._api.free_sequence(self._id, old_sequence.id)
                        # Update internal variable.
                        del allocated_sequences[old_sequence]
                        del allocated_sequence_counters[old_sequence]
                        available_memory = self._api.inquire_device(self._id, AVAIL_MEMORY)
                    if available_memory < sequence.size:
                        # TODO create exception (won't be able to display the sequence without any break).
                        raise NotImplementedError()
                    # Allocate sequence.
                    bit_planes = sequence.bit_planes
                    number_pictures = sequence.number_pictures
                    sequence_id = self._api.allocate_sequence(self._id, bit_planes, number_pictures)
                    # Update internal variables.
                    allocated_sequences[sequence] = sequence_id
                    allocated_sequence_counters[sequence] = 1
                    history.append(sequence)
                    # Control sequence.
                    for control_type, control_value in sequence.control_items:
                        self._api.control_sequence(self._id, sequence_id, control_type, control_value)
                    # Put sequence.
                    picture_offset = 0
                    data = sequence.data
                    self._api.put_sequence(self._id, sequence_id, picture_offset, number_pictures, data)

                # Start sequence.
                self._api.start_projection(self._id, sequence_id)

        except NotImplementedError:

            # Halt projection.
            self._api.halt_projection(self._id)

        finally:

            # Wait projection.
            self._api.wait_projection(self._id)
            # Free sequences.
            for sequence in allocated_sequences:
                sequence_id = allocated_sequences[sequence]
                self._api.free_sequence(self._id, sequence_id)

        return

    def display_white_frame(self, rate=20.0, duration=1.0) -> None:
        """Display a white frame."""

        white_frame_stimulus = WhiteFrameStimulus(self.height, self.width, rate, duration)
        self.display(white_frame_stimulus)

        return

    def display_white_frame_old(self, duration: float = 1.0) -> None:
        """Display a white frame.

        Argument:
            duration: float
                The duration of the white frame [s].
                The default value is 1.0.
        """

        # Inquire height and width.
        height = self._api.inquire_device(self._id, DEV_DISPLAY_HEIGHT)
        width = self._api.inquire_device(self._id, DEV_DISPLAY_WIDTH)
        print("height, width: {}, {}".format(height, width))
        # Allocate sequence.
        bit_planes = 8
        number_pictures = 100
        sequence_id = self._api.allocate_sequence(self._id, bit_planes, number_pictures)
        print("sequence_id: {}".format(sequence_id))
        # Put sequence.
        import numpy as np
        picture_offset = 0
        data = 255 * np.ones(number_pictures * height * width, dtype=np.uint8)
        self._api.put_sequence(self._id, sequence_id, picture_offset, number_pictures, data)
        print("put sequence")
        # Start sequence.
        self._api.start_projection(self._id, sequence_id)
        print("start projection")
        # Wait end of projection
        self._api.wait_projection(self._id)
        print("end projection")
        # Free sequence.
        self._api.free_sequence(self._id, sequence_id)
        print("free sequence")

        return

    def display_rectangle(self) -> None:

        print("Display rectangle...")

        # TODO inquire height and width.
        height = self._api.inquire_device(self._id, DEV_DISPLAY_HEIGHT)
        width = self._api.inquire_device(self._id, DEV_DISPLAY_WIDTH)
        print("height, width: {}, {}".format(height, width))
        # TODO allocate sequence.
        bit_planes = 8
        number_pictures = 100
        sequence_id = self._api.allocate_sequence(self._id, bit_planes, number_pictures)
        print("sequence_id: {}".format(sequence_id))
        # TODO put sequence.
        import numpy as np
        picture_offset = 0
        shape = (number_pictures, height, width)
        data = np.zeros(shape, dtype=np.uint8)
        i_min = (1 * width) // 4
        i_max = (3 * width) // 4
        j_min = (1 * height) // 4
        j_max = (3 * width) // 4
        data[:, j_min:j_max, i_min:i_max] = np.iinfo(np.uint8).max
        data = data.flatten()
        self._api.put_sequence(self._id, sequence_id, picture_offset, number_pictures, data)
        print("put sequence")
        # TODO start sequence.
        self._api.start_projection(self._id, sequence_id)
        print("start projection")
        # TODO wait end of projection
        self._api.wait_projection(self._id)
        print("end projection")
        # TODO free sequence.
        self._api.free_sequence(self._id, sequence_id)
        print("free sequence")

        return

    # def display_checkerboard(self) -> None:
    #
    #     print("Display checkerboard...")
    #
    #     # TODO complete.
    #
    #     return

    # def display_film(self) -> None:
    #
    #     print("Display film...")
    #
    #     # TODO complete.
    #
    #     return
