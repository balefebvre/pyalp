from typing import Optional

from .high import API as HighLevelAPI


def load_api(argument: Optional[str] = None) -> HighLevelAPI:

    if argument in [None, 'mock']:
        from .low.mock import API as MockLowLevelAPI
        api = MockLowLevelAPI()
    elif argument in ['alp', 'Alp', 'ALP']:
        from ctypes import cdll
        from os import environ
        from .low.alp import API as ALPLowLevelAPI
        path = environ['ALP_PATH']
        dll = cdll.LoadLibrary(path)
        api = ALPLowLevelAPI(dll)
    else:
        raise NotImplementedError()
    api = HighLevelAPI(api)

    return api
