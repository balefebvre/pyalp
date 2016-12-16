import ctypes
import os



# Constant values

## Special value
ALP_DEFAULT = 0
ALP_INVALID_ID = 2 ** 32 - 1 # ulong maximun

## Return value
ALP_OK = 0
ALP_NOT_ONLINE = 1001
ALP_NOT_IDLE = 1002
ALP_NOT_AVAILABLE = 1003
ALP_NOT_READY = 1004
ALP_PARM_INVALID = 1005
ALP_ADDR_INVALID = 1006
ALP_MEMORY_FULL = 1007
ALP_SEQ_IN_USE = 1008
ALP_HALTED = 1009
ALP_ERROR_INIT = 1010
ALP_ERROR_COMM = 1011
ALP_DEVICE_REMOVED = 1012
ALP_NOT_CONFIGURED = 1013
ALP_LOADER_VERSION = 1014
ALP_ERROR_POWER_DOWN = 1018

## Device inquire and control types
ALP_DEVICE_NUMBER = 2000
ALP_VERSION = 2001
ALP_AVAIL_MEMORY = 2003
ALP_SYNCH_POLARITY = 2004
ALP_LEVEL_HIGH = 2006
ALP_LEVEL_LOW = 2007
ALP_TRIGGER_EDGE = 2005
ALP_EDGE_FALLING = 2008
ALP_EDGE_RISING = 2009
ALP_DEV_DMDTYPE = 2021
ALP_DMDTYPE_XGA = 1
ALP_DMDTYPE_1080P_095A = 3
ALP_DMDTYPE_XGA_07A = 4
ALP_DMDTYPE_XGA_055X = 6
ALP_DMDTYPE_WUXGA_096A = 7
ALP_DMDTYPE_DISCONNECT = 255
# TODO check is these constant values exist...
# ALP_DMDTYPE_XGA_055A =
# ALP_DMDTYPE_SXGA_PLUS =
# ALP_DMDTYPE_WQXGA_400MHZ_090A =
# ALP_DMDTYPE_WQXGA_480MHZ_090A =
ALP_USB_CONNECTION = 2016
ALP_DEV_DYN_SYNCH_OUT1_GATE = 2023
ALP_DEV_DYN_SYNCH_OUT2_GATE = 2024
ALP_DEV_DYN_SYNCH_OUT3_GATE = 2025
ALP_DDC_FPGA_TEMPERATURE = 2050
ALP_APPS_FPGA_TEMPERATURE = 2051
ALP_PCB_TEMPERATURE = 2052
ALP_DEV_DISPLAY_HEIGHT = 2057
ALP_DEV_DISPLAY_WIDTH = 2058
ALP_PWM_LEVEL = 2063
ALP_DEV_DMD_MODE = 2064
ALP_DMD_POWER_FLOAT = 1

## Sequence inquire and control types
ALP_BITPLANES = 2200
ALP_BITNUM = 2103
ALP_BIN_MODE = 2104
ALP_BIN_NORMAL = 2105
ALP_BIN_UNINTERRUPTED = 2106
ALP_PICNUM = 2201
ALP_FIRSTFRAME = 2101
ALP_LASTFRAME = 2102
ALP_FIRSTLINE = 2111
ALP_LASTLINE = 2112
ALP_LINE_INC = 2113
ALP_SCROLL_FROM_ROW = 2123
ALP_SCROLL_TO_ROW = 2124
ALP_SEQ_REPEAT = 2100
ALP_PICTURE_TIME = 2203
ALP_MIN_PICTURE_TIME = 2211
ALP_MAX_PICTURE_TIME = 2213
ALP_ILLUMINATE_TIME = 2204
ALP_MIN_ILLUMINATE_TIME = 2212
ALP_ON_TIME = 2214
ALP_OFF_TIME = 2215
ALP_SYNCH_DELAY = 2205
ALP_MAX_SYNCH_DELAY = 2209
ALP_SYNCH_PULSEWIDTH = 2206
ALP_TRIGGER_IN_DELAY = 2207
ALP_MAX_TRIGGER_IN_DELAY = 2210
ALP_DATA_FORMAT = 2110
ALP_DATA_MSB_ALIGN = 0
ALP_DATA_LSB_ALIGN = 1
ALP_DATA_BINARY_TOPDOWN = 2
ALP_DATA_BINARY_BOTTOMUP = 3
ALP_SEQ_PUT_LOCK = 2117
ALP_FLUT_MODE = 2118
ALP_FLUT_NONE = 0
ALP_FLUT_9BIT = 1
ALP_FLUT_18BIT = 2
ALP_FLUT_ENTRIES9 = 2120
ALP_FLUT_OFFSET9 = 2122
ALP_PWM_MODE = 2107
ALP_FLEX_PWM = 3

## Projection inquire and control types
ALP_PROJ_MODE = 2300
ALP_MASTER = 2301
ALP_SLAVE = 2302
ALP_PROJ_STEP = 2329
ALP_PROJ_STATE = 2400
ALP_PROJ_ACTIVE = 1200
ALP_PROJ_IDLE = 1201
ALP_PROJ_INVERSION = 2306
ALP_PROJ_UPSIDE_DOWN = 2307
ALP_PROJ_QUEUE_MODE = 2314
ALP_PROJ_LEGACY = 0
ALP_PROJ_SEQUENCE_QUEUE = 1
ALP_PROJ_QUEUE_ID = 2315
ALP_PROJ_QUEUE_MAX_AVAIL = 2316
ALP_PROJ_QUEUE_AVAIL = 2317
ALP_PROJ_PROGRESS = 2318
ALP_FLAG_QUEUE_IDLE = 1
ALP_FLAG_SEQUENCE_ABORTING = 2
ALP_FLAG_SEQUENCE_INDEFINITE = 4
ALP_FLAG_FRAME_FINISHED = 8
ALP_PROJ_RESET_QUEUE = 2319
ALP_PROJ_ABORT_SEQUENCE = 2320
ALP_PROJ_ABORT_FRAME = 2321
ALP_PROJ_WAIT_UNTIL = 2323
ALP_PROJ_WAIT_PIC_TIME = 0
ALP_PROJ_WAIT_ILLU_TIME = 1
ALP_FLUT_MAX_ENTRIES9 = 2324
ALP_FLUT_WRITE_9BIT = 2325
ALP_FLUT_WRITE_18BIT = 2326

## LED types
ALP_HLD_PT120_RED = 257
ALP_HLD_PT120_GREEN = 258
ALP_HLD_PT120_BLUE = 259
ALP_HLD_PT120_UV = 260
ALP_HLD_CBT90_WHITE = 262
ALP_HLD_PT120TE_BLUE = 263
ALP_HLD_CBT140_WHITE = 264

## LED inquire and control types
ALP_LED_SET_CURRENT = 1001
ALP_LED_BRIGHTNESS = 1002
ALP_LED_FORCE_OFF = 1003
ALP_LED_AUTO_OFF = 0
ALP_LED_OFF = 1
ALP_LED_ON = 2
ALP_LED_TYPE = 1101
ALP_LED_MEASURED_CURRENT = 1102
ALP_LED_TEMPERATURE_REF = 1103
ALP_LED_TEMPERATURE_JUNCTION = 1104

## Extended LED inquire and control types
ALP_LED_ALLOC_PARAMS = 2101


class tAlpProjProgress(ctypes.Structure):
    _fields_ = [
        ('CurrentQueueId', ctypes.c_ulong),
        ('SequenceId', ctypes.c_ulong),
        ('nWaitingSequences', ctypes.c_ulong),
        ('nSequenceCounter', ctypes.c_ulong),
        ('nSequenceCounterUnderflow', ctypes.c_ulong),
        ('nFrameCounter', ctypes.c_ulong),
        ('nPictureTime', ctypes.c_ulong),
        ('nFramesPerSubSequence', ctypes.c_ulong),
        ('nFlags', ctypes.c_ulong),
    ]


def get_path():
    '''TODO add doc...'''
    try:
        alp_path = os.environ['ALP_PATH']
        return alp_path
    except KeyError as error:
        # TODO enhance message...
        message = "Environment variable ALP_PATH not found!"
        raise Exception(message)
        exit()


def load_api(path):
    '''TODO add doc...'''
    try:
        api = Api(path)
    except OSError as error:
        # TODO enhance message...
        message = "ALP DLL '{}' not found!".format(path)
        print(message)
        exit()


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
    '''Retrieve ALP API from DLL

    Parameter
    ---------
    path: string
        Path to the ALP DLL file.

    TODO complete...
    '''
    def __init__(self, path):
        '''TODO add doc...'''
        self.path = path
        self.dll = ctypes.cdll.LoadLibrary(self.path)

    def __del__(self):
        try:
            del self.dll
        except AttributeError: # in case ctypes.cdll.LoadLibrary failed
            pass
        del self.path
        return

    def __getattribute__(self, name):
        '''TODO add doc...'''
        if name in function_names:
            attribute = object.__getattribute__(self.dll, name)
        else:
            attribute = object.__getattribute__(self, name)
        return attribute
