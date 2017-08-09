import numpy

import pyalp.io

from .base import Sequence


class Film(Sequence):
    """Film sequence.

    Parameters
    ----------
    sequence_id: integer
        Sequence identifier.
    bin_pathname: string
        Pathname to the .bin file.
    frame_ids: numpy.ndarray
        Vector of frame identifiers.
    nb_frames: integer
        Number of frames in the sequence.
    sequence_size: integer
        Maximal number of frames in the sequence.
    rate: float
        Frame rate [Hz].

    """

    def __init__(self, sequence_id, bin_pathname, image_ids, nb_frames, sequence_size, rate):

        bit_planes = 8
        pic_num = nb_frames
        picture_time = int(1.0e+6 / rate)
        Sequence.__init__(self, bit_planes, pic_num, picture_time=picture_time)

        self.sequence_id = sequence_id
        self.bin_pathname = bin_pathname
        self.image_ids = image_ids
        self.nb_frames = nb_frames
        self.sequence_size = sequence_size
        self.rate = rate

        self.bin_header = pyalp.io.load_bin_header(self.bin_pathname)
        self.header_size = self.bin_header['size']
        self.width = self.bin_header['width']
        self.height = self.bin_header['height']
        self.image_shape = (self.height, self.width)
        self.image_size = self.height * self.width

    def get_user_array(self):
        """Get stimulus frames."""

        # Allocate frames.
        width, height = self.device.get_resolution()
        shape = (self.nb_frames, height, width)
        dtype = numpy.uint8
        frames = numpy.zeros(shape, dtype=dtype)

        # Generate data.
        start_frame_id = self.sequence_id * self.sequence_size
        end_frame_id = start_frame_id + self.nb_frames
        with open(self.bin_pathname, mode='rb') as bin_fid:
            for k, frame_id in enumerate(range(start_frame_id, end_frame_id)):
                image_id = self.image_ids[frame_id]
                offset = self.header_size + image_id * self.image_size
                bin_fid.seek(offset)
                frame = numpy.fromfile(bin_fid, dtype=numpy.uint8, count=self.image_size)
                frame = numpy.reshape(frame, self.image_shape)
                frames[k, :, :] = frame

        return frames
