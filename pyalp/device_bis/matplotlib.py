from multiprocessing import Pipe
# from multiprocessing.sharedctypes import RawArray
from queue import Empty

from .base import Device as BaseDevice
# from ..module import MatplotlibModule
# from ..dmd import MatplotlibDMD
from .dmd.matplotlib import DMD


class Device(BaseDevice):
    """Matplotlib device."""

    def __init__(self):
        """Initialize a Matplotlib device."""

        # usb_connection_1, usb_connection_2 = Pipe()
        # bus_connection_1, bus_connection_2 = Pipe()
        # memory = RawArray('B', 100000000)  # unsigned char
        #
        # self._device_number = None
        # self._usb_connection = usb_connection_1
        # self._module = MatplotlibModule(usb_connection_2, bus_connection_1, memory)
        # self._dmd = MatplotlibDMD(bus_connection_2, memory)

        # TODO replace by the previous lines by the following ones.

        connection_1, connection_2 = Pipe()

        self._usb_connection = connection_1
        self._dmd = DMD(connection_2)

        return

    def turn_on(self):
        # TODO add docstring.

        # self._module.start()  # TODO remove line.
        self._dmd.start()

        return

    def turn_off(self):
        # TODO add docstring.

        # self._module.join()  # TODO remove line.
        self._dmd.join()

        return

    def allocate(self, device_number=0):
        # TODO add docstring.

        self._device_number = device_number

        self._send_usb({
            'command': 'allocate',
        })
        _ = self._receive_usb()

        return

    def control(self, control_type, control_value):
        # TODO add docstring.

        self._send_usb({
            'command': 'control',
            'control_type': control_type,
            'control_value': control_value,
        })
        _ = self._receive_usb()

        return

    def inquire(self, inquire_type):
        # TODO add docstring.

        self._send_usb({
            'command': 'inquire',
            'inquire_type': inquire_type,
        })
        response = self._receive_usb()
        inquire_value = response['inquire_value']

        return inquire_value

    def halt(self):
        # TODO add docstring.

        self._send_usb({
            'command': 'halt',
        })
        _ = self._receive_usb()

        return

    def get(self):
        # TODO add docstring.

        self._send_usb({
            'command': 'get',
        })
        _ = self._receive_usb()

        return

    def set(self):
        # TODO add docstring.

        self._send_usb({
            'command': 'set',
        })
        obj = self._receive_usb()

        return obj

    def free(self):
        # TODO add docstring.

        self._send_usb({
            'command': 'free',
        })
        _ = self._receive_usb()

        return

    # TODO remove following method.
    def display(self):
        # TODO add docstring.

        self._send_usb({
            'command': 'display',
        })
        _ = self._receive_usb()

        return

    def allocate_sequence(self, bit_planes, number_pictures):

        self._send_usb({
            'command': 'allocate_sequence',
            'bit_planes': bit_planes,
            'number_pictures': number_pictures,
        })
        response = self._receive_usb()
        sequence_id = response['sequence_id']

        return sequence_id

    def control_sequence(self, sequence_id, control_type, control_value):
        # TODO add docstring.

        # TODO complete.

        return

    def control_timing_sequence(self):

        # TODO merge with previous method.

        return

    def inquire_sequence(self, sequence_id, inquire_type):
        # TODO add docstring.

        # TODO complete.

        return

    def put_sequence(self, sequence_id, picture_offset, number_pictures, data):
        # TODO add docstring.

        self._send_usb({
            'command': 'put_sequence',
            'sequence_id': sequence_id,
            'picture_offset': picture_offset,
            'number_pictures': number_pictures,
            'data': data,
        })
        _ = self._receive_usb()

        return

    def free_sequence(self, sequence_id):
        # TODO add docstring.

        self._send_usb({
            'command': 'free_sequence',
            'sequence_id': sequence_id,
        })
        _ = self._receive_usb()

        return

    def start_projection(self, sequence_id):
        # TODO add docstring.

        self._send_usb({
            'command': 'start_projection',
            'sequence_id': sequence_id,
        })
        _ = self._receive_usb()

        return

    def _send_usb(self, obj):
        # TODO add docstring.

        self._usb_connection.send(obj)

        return

    def _receive_usb(self, timeout=None):

        if self._usb_connection.poll(timeout=timeout):
            obj = self._usb_connection.recv()
        else:
            raise Empty

        return obj
