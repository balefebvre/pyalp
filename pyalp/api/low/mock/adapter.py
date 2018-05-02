from ....device_ter.mock import Device
from ..error import *
from .constant import *


class Adapter:

    def __init__(self):

        self._devices = {}

        return

    def _send(self, device_id: int, args: dict) -> dict:

        if device_id in self._devices:
            device = self._devices[device_id]
            connection = device.get_connection()
            connection.send(args)
            ans = connection.recv()
        else:
            raise NotImplementedError()

        return ans

    def dev_alloc(self, device_number: int, init_flag: int):

        if device_number not in self._devices:
            device = Device(device_number)
            device.start()
            self._devices[device_number] = device

        # Prepare arguments.
        device_id = device_number
        args = dict(
            function='dev_alloc',
            init_flag=init_flag,
        )
        # Call function.
        ans = self._send(device_id, args)
        # Handle error (if necessary).
        print(ans)
        ret_val = ans['ret_val']
        if ret_val == MOCK_OK:
            pass
        elif ret_val == MOCK_ADDR_INVALID:
            raise AddrInvalidError()
        elif ret_val == MOCK_NOT_ONLINE:
            raise NotOnlineError()
        elif ret_val == MOCK_NOT_READY:
            raise NotReadyError()
        elif ret_val == MOCK_ERROR_INIT:
            raise InitError()
        elif ret_val == MOCK_LOADER_VERSION:
            raise LoaderVersionError()
        elif ret_val == MOCK_ERROR_COMM:
            raise CommError()
        elif ret_val == MOCK_DEVICE_REMOVED:
            raise DeviceRemovedError()
        else:
            raise NotImplementedError(ret_val)
        # Prepare result.
        device_id = ans['payload']

        return device_id

    def dev_halt(self, device_id):
        """Put the mock in an idle wait state.

        Argument:
            device_id: int
                Mock identifier of the device to be freed.
        """

        # Prepare arguments.
        args = dict(
            function='dev_halt',
        )
        # Call function.
        ans = self._send(device_id, args)
        # Handle error (if necessary).
        ret_val = ans['ret_val']
        if ret_val == MOCK_OK:
            pass
        elif ret_val == MOCK_NOT_AVAILABLE:
            raise NotAvailableError()
        else:
            raise NotImplementedError(ret_val)

        return

    def dev_free(self, device_id: int) -> None:
        """De-allocate a previously allocated mock device.

        Argument:
            device_id: int
                Mock identifier of the device to be freed.
        """

        # Prepare arguments.
        args = dict(
            function='dev_free',
        )
        # Call function.
        ans = self._send(device_id, args)
        # Handle error (if necessary).
        ret_val = ans['ret_val']
        if ret_val == MOCK_OK:
            pass
        elif ret_val == MOCK_NOT_AVAILABLE:
            raise NotAvailableError()
        elif ret_val == MOCK_NOT_READY:
            raise NotReadyError()
        elif ret_val == MOCK_NOT_IDLE:
            raise NotIdleError()
        else:
            raise NotImplementedError(ret_val)

        return

    def seppuku(self) -> None:

        for device in self._devices.values():
            device.seppuku()

        return
