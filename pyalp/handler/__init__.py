from typing import Optional

from ..api.high import API
from .device import DeviceHandler


def handle_device(serial_number: Optional[int] = None, api: Optional[API] = None) -> DeviceHandler:
    # TODO add docstring.

    handler = DeviceHandler(serial_number=serial_number, api=api)

    return handler
