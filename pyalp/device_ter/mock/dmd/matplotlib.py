from multiprocessing import Process, Pipe, Event
from multiprocessing.sharedctypes import RawArray
from queue import Empty
from signal import getsignal, signal, SIG_IGN, SIGINT

from .base import DMD as BaseDMD
# from ..module import MatplotlibModule  # TODO remove line.
# from ..dmd import MatplotlibDMD  # TODO remove line.
from ..controller.matplotlib import Controller


class DMD(Process, BaseDMD):
    """Matplotlib DMD."""

    def __init__(self, connection):
        """Initialize Matplotlib DMD.

        Argument:
            connection: multiprocessing.Connection
        """

        super().__init__()

        connection_1, connection_2 = Pipe()
        memory = RawArray('B', 100000000)  # unsigned char

        self._usb_connection = connection
        self._bus_connection = connection_1
        self._memory = memory
        self._controller = Controller(connection_2, memory)
        # self._module = MatplotlibModule(usb_connection_2, bus_connection_1, memory)  # TODO remove line.
        # self._dmd = MatplotlibDMD(bus_connection_2, memory)  # TODO remove line.

        self._dmd_type = '1080P_095A'
        self._width = 1920
        self._height = 1080
        self._is_allocated = Event()
        self._sequences = {}

        return

    def run(self):
        # TODO add docstring.

        # ...
        while not self._is_allocated.is_set():
            try:
                self._process()
            except Empty:
                continue
        # ...
        while self._is_allocated.is_set():
            try:
                self._process()
            except Empty:
                continue

        return

    def start(self):
        # TODO add docstring.

        # NB signals are propagated down the process tree. See also:
        #   https://vimmaniac.com/blog/codejunkie/safe-use-of-unix-signals-with-multiprocessing-module-in-python

        # Set signal handling to ignore mode for child processes.
        sigint_handler = getsignal(SIGINT)
        signal(SIGINT, SIG_IGN)

        super().start()

        # Restore default signal handling for parent process.
        signal(SIGINT, sigint_handler)

        self._controller.start()

        return

    def _process(self):
        # TODO add docstring.

        request = self._receive_usb(timeout=0.1)

        function_ = request.get('function', None)

        if function_ == 'dev_alloc':
            response = self._allocate(request)
        elif function_ == 'dev_inquire':
            response = self._inquire(request)
        elif function_ == 'dev_free':
            response = self._free(request)
        elif function_ == 'dev_display':
            response = self._display(request)
        elif function_ == 'seq_alloc':
            response = self._allocate_sequence(request)
        elif function_ == 'seq_put':
            response = self._put_sequence(request)
        elif function_ == 'seq_free':
            response = self._free_sequence(request)
        elif function_ == 'proj_start':
            response = self._start_projection(request)
        else:
            self._send_bus(request)
            response = self._receive_bus()

        self._send_usb(response)

        return

    def _allocate(self, request):
        # TODO add docstring.

        self._is_allocated.set()
        self._send_bus(request)
        response = self._receive_bus()

        return response

    def _inquire(self, request):
        # TODO add docstring.

        inquire_type = request['inquire_type']

        if inquire_type == 'dmd_type':
            inquire_value = '1080P_095A'
        else:
            inquire_value = None

        response = {
            'inquire_value': inquire_value,
        }

        return response

    def _free(self, request):
        # TODO add docstring.

        self._is_allocated.clear()
        self._send_bus(request)
        response = self._receive_bus()

        return response

    def _display(self, request):
        # TODO add docstring.

        self._send_bus(request)
        response = self._receive_bus()

        return response

    def _allocate_sequence(self, request):
        # TODO add docstring.

        bit_planes = request['bit_planes']
        number_pictures = request['number_pictures']

        # TODO check bit_planes value (integer between 1 and 8).
        # TODO check number_pictures values.

        size = self._width * self._height * number_pictures  # bytes

        _ = size  # TODO complete.

        sequence_id = 0

        self._sequences[sequence_id] = {
            'start_picture_id': 0,
            'bit_planes': bit_planes,
            'number_pictures': number_pictures,
        }

        response = {
            'sequence_id': sequence_id,
        }

        return response

    def _put_sequence(self, request):

        sequence_id = request['sequence_id']
        picture_offset = request['picture_offset']
        number_pictures = request['number_pictures']
        data = request['data']

        if sequence_id in self._sequences:

            sequence = self._sequences[sequence_id]
            start_picture_id = sequence['start_picture_id']
            start_picture_id += picture_offset
            end_picture_id = start_picture_id + number_pictures
            start_address = start_picture_id * self._height * self._width
            end_address = end_picture_id * self._height * self._width
            self._memory[start_address:end_address] = data

        # TODO complete.

        return {}

    def _free_sequence(self, request):

        sequence_id = request['sequence_id']

        if sequence_id in self._sequences:
            del self._sequences[sequence_id]

        # TODO complete (e.g. check if sequence is displayed).

        return {}

    def _start_projection(self, request):

        sequence_id = request['sequence_id']

        if sequence_id in self._sequences:

            sequence = self._sequences[sequence_id]
            request.update(sequence)

            self._send_bus(request)

        return {}

    def _receive_usb(self, timeout=0.0):
        # TODO add docstring.

        if self._usb_connection.poll(timeout=timeout):
            obj = self._usb_connection.recv()
        else:
            raise Empty

        return obj

    def _send_usb(self, obj):
        # TODO add docstring.

        self._usb_connection.send(obj)

        return

    def _send_bus(self, obj):
        # TODO add docstring.

        self._bus_connection.send(obj)

        return

    def _receive_bus(self, timeout=None):
        # TODO add docstring.

        if self._bus_connection.poll(timeout=timeout):
            obj = self._bus_connection.recv()
        else:
            raise Empty

        return obj
