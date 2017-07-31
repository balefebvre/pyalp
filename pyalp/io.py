import numpy as np


def load_vec(pathname):
    """TODO add docstring."""

    dtype = int  # data-type
    usecols = (1,)  # extract only the 2nd column
    x = np.loadtxt(pathname, dtype=dtype, usecols=usecols)

    nb_frames = x[0]  # e.g. header
    frame_ids = x[1:]  # e.g. body
    assert len(frame_ids) == nb_frames

    return frame_ids


def load_bin_header(pathname):
    """TODO add docstring"""

    header = dict()

    with open(pathname, mode='rb') as fid:
        header['width'] = int.from_bytes(fid.read(2), byteorder='little')
        header['height'] = int.from_bytes(fid.read(2), byteorder='little')
        header['nb_images'] = int.from_bytes(fid.read(2), byteorder='little')
        header['nb_bits'] = int.from_bytes(fid.read(2), byteorder='little')

    return header
