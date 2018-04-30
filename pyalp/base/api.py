import ctypes
import os


function_names = [
    'AlpDevAlloc',
    'AlpDevControl',
    'AlpDevInquire',
    'AlpDevControlEx',
    'AlpDevHalt',
    'AlpDevFree',
    'AlpSeqAlloc',
    'AlpSeqControl',
    'AlpSeqTiming',
    'AlpSeqInquire',
    'AlpSeqPut',
    'AlpSeqFree',
    'AlpProjControl',
    'AlpProjInquire',
    'AlpProjControlEx',
    'AlpProjInquireEx',
    'AlpProjStart',
    'AlpProjStartCont',
    'AlpProjHalt',
    'AlpProjWait',
    'AlpLedAlloc',
    'AlpLedFree',
    'AlpLedControl',
    'AlpLedInquire',
    'AlpLedControlEx',
    'AlpLedInquireEx',
]


class Api(object):
    """Retrieve ALP API from DLL.

    Parameter
    ---------
    path: string
        Path to the ALP DLL file.

    TODO complete.
    """
    def __init__(self, pathname):
        """TODO add docstring."""
        self.pathname = pathname
        self.dll = ctypes.cdll.LoadLibrary(self.pathname)

    def __del__(self):
        try:
            del self.dll
        except AttributeError:  # in case ctypes.cdll.LoadLibrary failed
            pass
        del self.pathname
        return

    def __getattribute__(self, function_name):
        """TODO add docstring."""
        if function_name in function_names:
            attribute = getattr(self.dll, function_name)
        else:
            attribute = object.__getattribute__(self, function_name)
        return attribute


# Retrieve ViALUX ALP path.
try:
    path = os.environ['ALP_PATH']
except KeyError:
    message = "Environment variable ALP_PATH not found!"
    raise Exception(message)


# Load ViALUX ALP API.
try:
    api = Api(path)
except OSError:
    message = "ALP DLL '{}' not found!".format(path)
    raise Exception(message)
