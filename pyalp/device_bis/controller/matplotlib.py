import matplotlib.pyplot as plt
import numpy as np

from multiprocessing import Process, Event
from queue import Empty
from signal import getsignal, signal, SIG_IGN, SIGINT
from tkinter import TclError

from .base import Controller as BaseController


class Controller(Process, BaseController):
    """Matplotlib controller."""

    def __init__(self, connection, memory):
        """Initialize a Matplotlib controller.

        Arguments:
            connection: multiprocessing.Connection
        """

        super().__init__()

        self._bus_connection = connection
        self._memory = memory

        self._height = 1080
        self._width = 1920
        self._shape = (self._height, self._width)
        self._cmap = 'gray'  # or 'binary'
        self._image = None
        self._figure = None
        self._is_allocated = Event()

        return

    def run(self):

        try:
            # ...
            while not self._is_allocated.is_set():
                try:
                    self._process()
                except Empty:
                    continue
            # ...
            self._create_figure()
            # ...
            while self._is_allocated.is_set():
                plt.pause(0.001)
                try:
                    self._process()
                except Empty:
                    continue
            # ...
            self._destroy_figure()
        except TclError:
            print("TclError...")

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

        return

    def _create_figure(self):
        # TODO add docstring.

        plt.ion()
        self._figure = plt.figure()
        data = np.zeros(self._shape)
        self._image = plt.imshow(data, cmap=self._cmap, vmin=0, vmax=255)
        plt.draw()
        # plt.show(block=False)
        # Move the window lower in the window stack.
        self._figure.canvas.manager.window.lower()
        plt.pause(0.001)

        return

    def _destroy_figure(self):
        # TODO add docstring.

        if self._figure is not None:
            plt.close(self._figure)
            self._image = None
            self._figure = None

        return

    def _process(self):
        # TODO add docstring.

        request = self._receive_bus(timeout=0.1)

        command = request.get('command', None)

        if command == 'allocate':
            self._is_allocated.set()
            response = {}
            self._send_bus(response)
        elif command == 'free':
            self._is_allocated.clear()
            response = {}
            self._send_bus(response)
        elif command == 'display':
            import time
            shape = self._shape + (100,)
            data = np.random.random_integers(0, 1, shape)
            start_time = time.time()
            for i in range(0, 100):
                self._image.set_data(data[:, :, i])
                plt.draw()
                plt.pause(0.001)
            end_time = time.time()
            duration = end_time - start_time
            print("duration: {} s".format(duration))
            print("frequency: {} Hz".format(float(100) / duration))
            data = np.zeros(self._shape)
            self._image.set_data(data)
            plt.draw()
            plt.pause(0.001)
            response = {}
            self._send_bus(response)
        elif command == 'start_projection':
            self._start_projection(request)
        else:
            response = {}
            self._send_bus(response)

        return

    def _start_projection(self, request):

        start_picture_id = request['start_picture_id']
        number_pictures = request['number_pictures']
        end_picture_id = start_picture_id + number_pictures

        for picture_id in range(start_picture_id, end_picture_id):
            start_address_id = picture_id * self._height * self._width
            end_address_id = (picture_id + 1) * self._height * self._width
            data = self._memory[start_address_id:end_address_id]
            data = np.reshape(data, self._shape)
            self._image.set_data(data)
            plt.draw()
            plt.pause(0.1)
        data = np.zeros(self._shape)
        self._image.set_data(data)
        plt.draw()
        plt.pause(0.001)

        # TODO display pictures stored in memory.

        return {}

    def _receive_bus(self, timeout=0.1):
        # TODO add docstring.

        if self._bus_connection.poll(timeout=timeout):
            obj = self._bus_connection.recv()
        else:
            raise Empty

        return obj

    def _send_bus(self, obj):
        # TODO add docstring.

        self._bus_connection.send(obj)

        return
