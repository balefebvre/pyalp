from multiprocessing import Pipe

from .dmd.matplotlib import DMD


class Device:

    def __init__(self, device_number):

        self._device_number = device_number

        connection_1, connection_2 = Pipe()

        self._usb_connection = connection_1
        self._dmd = DMD(connection_2)

    def get_connection(self):

        return self._usb_connection

    def start(self):

        self._dmd.start()

        return

    def seppuku(self):

        self._dmd.join()

        return
