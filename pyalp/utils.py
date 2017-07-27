import builtins
import ctypes
import numpy



def numpy_to_ctypes(a):
    '''TODO add doc...'''
    s = a.tobytes()
    # size = a.shape[0]
    size = a.size
    # print("size: {}".format(size))
    # print("a[:5]: {}".format(a[:5]))
    # print("a.size: {}".format(a.size))
    b = ctypes.create_string_buffer(s, size)
    return b

def get_black_frame(dmd_width, dmd_height, dtype='uint8'):
    '''TODO add doc...'''
    dmd_size = dmd_width * dmd_height
    f_min, _, f_dtype = numpy.iinfo(dtype)
    frame = f_min * numpy.ones(dmd_size, dtype=f_dtype)
    frame = numpy_to_ctypes(frame)
    return frame

def get_white_frame(dmd_width, dmd_height, dtype='uint8'):
    '''TODO add doc...'''
    dmd_size = dmd_width * dmd_height
    _, f_max, f_dtype = numpy.iinfo(dtype)
    frame = f_max * numpy.ones(dmd_size, dtype=f_dtype)
    frame = numpy_to_ctypes(frame)
    return frame

def get_flicker_frames(dmd_width, dmd_height, dtype='uint8'):
    '''TODO add doc...'''
    dmd_size = dmd_width * dmd_height
    f_min, f_max, f_dtype = numpy.iinfo(dtype)
    black_frame = f_min * numpy.ones(dmd_size, dtype=f_dtype)
    white_frame = f_max * numpy.zeros(dmd_size, dtype=f_dtype)
    frames = numpy.concatenate((black_frame, white_frame))
    frames = numpy_to_ctypes(frames)
    return frames

def get_full_field_frames(fingerprint, dmd_width, dmd_height, dtype='uint8'):
    '''TODO add doc...'''
    assert(fingerprint.dtype == dtype)
    dmd_size = dmd_width * dmd_height
    repeater = numpy.ones(dmd_size, dtype=dtype)
    frames = numpy.kron(fingerprint, repeater)
    frames = numpy_to_ctypes(frames)
    return frames

def get_moving_bars_frames(dmd_width, dmd_height, dtype='uint8'):
    '''TODO add doc...'''
    # TODO generate boolean frames...
    return frames

def input(prompt, callback):
    '''TODO add doc string'''
    ans = None
    while ans is None:
        try:
            arg = builtins.input(prompt)
            ans = callback(arg)
        except:
            print("  Input error, try again...")
    return ans