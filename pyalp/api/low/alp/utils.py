from ctypes import create_string_buffer

from numpy import ndarray


def c_ubyte_array(array: ndarray):

    string = array.tobytes()
    size = len(string)
    array_ = create_string_buffer(string, size)

    return array_
