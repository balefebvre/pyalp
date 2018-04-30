import abc
import numpy as np

from .device_bis import MatplotlibDevice


def handle(mock=False, device_number=0):
    # TODO add docstring.

    if mock:
        handle_ = MatplotlibHandle(device_number=device_number)
    else:
        handle_ = ALPHandle(device_number=device_number)

    return handle_


class Handle(metaclass=abc.ABCMeta):
    # TODO add docstring.

    @abc.abstractmethod
    def __init__(self):

        pass

    @abc.abstractmethod
    def release(self):

        raise NotImplementedError()


class MatplotlibHandle(Handle):
    # TODO add docstring.

    def __init__(self, device_number=0):
        # TODO add docstring.

        super().__init__()

        self._device = MatplotlibDevice()
        self._device.turn_on()
        self._device.allocate(device_number)

        self._is_active = True

        return

    def release(self):
        # TODO add docstring.

        if self._is_active:
            self._device.halt()  # TODO execute line if necessary only.
            self._device.free()
            self._device.turn_off()
            self._is_active = False
        else:
            pass  # TODO raise warning.

        return

    def display(self):
        # TODO add docstring.

        print("MatplotlibHandle: display")
        self._device.display()

        return

    def checkerboard(self):
        # TODO add docstring.

        try:
            # TODO inquire DMD type.
            dmd_type = self._device.inquire('dmd_type')
            if dmd_type == '1080P_095A':
                width = 1920
                height = 1080
            else:
                raise NotImplementedError()
            print(dmd_type)
            # TODO allocate sequence.
            bit_planes = 8
            number_pictures = 10
            sequence_id = self._device.allocate_sequence(bit_planes, number_pictures)
            # TODO put first sequence.
            picture_offset = 0
            data = 255 * np.random.random_integers(0, 1, number_pictures * height * width)
            self._device.put_sequence(sequence_id, picture_offset, number_pictures, data)
            # TODO start first sequence.
            self._device.start_projection(sequence_id)
            # TODO sleep
            # TODO free sequence.
            self._device.free_sequence(sequence_id)

            # TODO allocate device (not necessary).
            # TODO inquire device type (not necessary).
            # TODO prompt input arguments (if necessary).
            # TODO read binary file.
            # TODO allocate 1st sequence.
            # TODO control 1st sequence.
            # TODO allocate 2nd sequence.
            # TODO control 2nd sequence.
            # TODO projection on DMD.
            # TODO   control projection.
            # TODO   put 1st sequence.
            # TODO   start 1st sequence.
            # TODO   put 2nd sequence.
            # TODO   start 2nd sequence.
            # TODO   while ...
            # TODO     wait end of 1st sequence.
            # TODO     free 1st sequence.
            # TODO     allocate 1st sequence.
            # TODO     control 1st sequence.
            # TODO     put 1st sequence.
            # TODO     start 1st sequence.
            # TODO     <idem for 2nd sequence>
            # TODO halt projection.
            # TODO free device (not necessary).
            pass
        except KeyboardInterrupt:
            pass

        print("Not implemented...")


class ALPHandle(Handle):
    # TODO add docstring.

    def __init__(self, device_number=0):
        # TODO add docstring.

        super().__init__()

        self._device_number = device_number

        # TODO allocate device.

    def release(self):
        # TODO add docstring.

        raise NotImplementedError()
