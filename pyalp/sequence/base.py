from ctypes import c_ulong, byref

from ..base import api
from ..base.constant import *


class Sequence(object):
    """Sequence base class.

    Parameters
    ----------
    bit_planes: integer
    pic_num: integer
    ...

    """
    # TODO complete docstring.

    def __init__(self, bit_planes, pic_num, pic_offset=ALP_DEFAULT, pic_load=ALP_DEFAULT, illuminate_time=ALP_DEFAULT,
                 picture_time=ALP_DEFAULT, synch_delay=ALP_DEFAULT, synch_pulse_width=ALP_DEFAULT,
                 trigger_in_delay=ALP_DEFAULT):
        # Save input parameters
        self.bit_planes = bit_planes
        self.pic_num = pic_num
        self.pic_offset = pic_offset
        self.pic_load = pic_load
        self.illuminate_time = illuminate_time
        self.picture_time = picture_time
        self.synch_delay = synch_delay
        self.synch_pulse_width = synch_pulse_width
        self.trigger_in_delay = trigger_in_delay
        # Save additional parameter
        self.id = ALP_DEFAULT
        self.device = None
        self.infinite_loop = False
        self.bit_num = None
        self.bin_mode = None
        self.first_frame = None
        self.last_frame = None
        self.sequence_repeat = None
        self.min_picture_time = None
        self.max_picture_time = None
        self.min_illuminate_time = None
        self.on_time = None
        self.off_time = None
        self.data_format = None
        self.sequence_put_lock = None

    def is_finite(self):
        """TODO add doc..."""

        return not self.infinite_loop

    def inquire(self, inquire_type):
        """Inquire a parameter setting on the picture sequence"""
        device_id_ = c_ulong(self.device.id)
        sequence_id_ = c_ulong(self.id)
        inquire_type_ = c_ulong(inquire_type)
        user_var_ = c_ulong(ALP_DEFAULT)
        user_var_ptr_ = byref(user_var_)
        ret_val_ = api.AlpSeqInquire(device_id_, sequence_id_, inquire_type_, user_var_ptr_)
        if ret_val_ == ALP_OK:
            ret_val_ = user_var_.value
            return ret_val_
        else:
            raise Exception("AlpSeqInquire: {}".format(ret_val_))

    def inquire_bit_planes(self):
        """Inquire the bit depth of the pictures in the sequence"""
        self.bit_planes = self.inquire(ALP_BITPLANES)
        return self.bit_planes

    def inquire_bit_num(self):
        """Inquire the bit depth for display"""
        self.bit_num = self.inquire(ALP_BITNUM)
        return self.bit_num

    def inquire_bin_mode(self):
        """Inquire the status of the binary mode for display"""
        self.bin_mode = self.inquire(ALP_BIN_MODE)
        return self.bin_mode

    def inquire_pic_num(self):
        """Inquire the number of pictures in the sequence"""
        self.pic_num = self.inquire(ALP_PICNUM)
        return self.pic_num

    def inquire_first_frame(self):
        """Inquire the number of the first picture in the sequence selected for display"""
        self.first_frame = self.inquire(ALP_FIRSTFRAME)
        return self.first_frame

    def inquire_last_frame(self):
        """Inquire the number of the last picture in the sequence selected for display"""
        self.last_frame = self.inquire(ALP_LASTFRAME)
        return self.last_frame

    # TODO add inquiry for ALP_SCROLL_FROM_ROW, ALP_SCROLL_TO_ROW,
    # ALP_FIRSTLINE, ALP_LASTLINE, ALP_LINE_INC

    def inquire_sequence_repeat(self):
        """Inquire the number of automatically repeated displays of the sequence"""
        self.sequence_repeat = self.inquire(ALP_SEQ_REPEAT)
        return self.sequence_repeat

    def inquire_picture_time(self):
        """Inquire the time between the start of consecutive pictures"""
        self.picture_time = self.inquire(ALP_PICTURE_TIME)
        return self.picture_time

    def inquire_min_picture_time(self):
        """Inquire the minimum time between the start of consecutive pictures"""
        self.min_picture_time = self.inquire(ALP_MIN_PICTURE_TIME)
        return self.min_picture_time

    def inquire_max_picture_time(self):
        """Inquire the maximum time between the start of consecutive pictures"""
        self.max_picture_time = self.inquire(ALP_MAX_PICTURE_TIME)
        return self.max_picture_time

    def inquire_illuminate_time(self):
        """Inquire the duration of the display of one picture"""
        self.illuminate_time = self.inquire(ALP_ILLUMINATE_TIME)
        return self.illuminate_time

    def inquire_min_illuminate_time(self):
        """Inquire the minimum duration of the display of one picture"""
        self.min_illuminate_time = self.inquire(ALP_MIN_ILLUMINATE_TIME)
        return self.min_illuminate_time

    def inquire_on_time(self):
        """Inquire the total active projection time"""
        self.on_time = self.inquire(ALP_ON_TIME)
        return self.on_time

    def inquire_off_time(self):
        """Inquire the total inactive projection time"""
        self.off_time = self.inquire(ALP_OFF_TIME)
        return self.off_time

    # TODO add inquiry for ALP_SYNCH_DELAY, ALP_MAX_SYNCH_DELAY,
    # ALP_SYNCH_PULSEWIDTH, ALP_TRIGGER_IN_DELAY, ALP_MAX_TRIGGER_IN_DELAY

    def inquire_data_format(self):
        """Inquire the active image data format"""
        self.data_format = self.inquire(ALP_DATA_FORMAT)
        return self.data_format

    def inquire_sequence_put_lock(self):
        """Inquire the status of the lock protecting sequence data against
        writing during display"""
        self.sequence_put_lock = self.inquire(ALP_SEQ_PUT_LOCK)
        return self.sequence_put_lock

    # TODO add inquiry for ALP_FLUT_MODE, ALP_FLUT_ENTRIES9, ALP_FLUT_OFFSET9

    # TODO add inquiry for ALP_PWM_MODE

    def inquire_settings(self):
        settings = {
            'bit planes': self.inquire_bit_planes(),
            'bit num': self.inquire_bit_num(),
            'bin mode': self.inquire_bin_mode(),
            'pic num': self.inquire_pic_num(),
            'first frame': self.inquire_first_frame(),
            'last frame': self.inquire_last_frame(),
            # TODO complete...
            'sequence repeat': self.inquire_sequence_repeat(),
            'picture time': self.inquire_picture_time(),
            'min picture time': self.inquire_min_picture_time(),
            'max picture time': self.inquire_max_picture_time(),
            'illuminate time': self.inquire_illuminate_time(),
            'min illuminate time': self.inquire_min_illuminate_time(),
            'on time': self.inquire_on_time(),
            'off time': self.inquire_off_time(),
            # TODO complete...
            'data format': self.inquire_data_format(),
            # 'sequence put lock': self.inquire_sequence_put_lock(device),
            # TODO complete...
        }
        return settings

    def control(self, control_type, control_value):
        """TODO add docstring."""

        self.device.control_sequence(self, control_type, control_value)

        return

    def control_nb_repetitions(self, nb_repetitions):
        """TODO add docstring."""

        self.control(ALP_SEQ_REPEAT, nb_repetitions)

        return

    def control_bit_number(self, bit_number):
        """TODO add docstring."""

        self.control(ALP_BITNUM, bit_number)

        return

    def control_binary_mode(self, binary_mode):
        """TODO add docstring."""

        if binary_mode is 'normal':
            self.control(ALP_BIN_MODE, ALP_BIN_NORMAL)
        elif binary_mode is 'uninterrupted':
            self.control(ALP_BIN_MODE, ALP_BIN_UNINTERRUPTED)
        else:
            raise NotImplementedError()

        return

    def control_timing(self):
        """TODO add docstring"""

        self.device.control_timing(self)

        return

    def load(self):
        """TODO add docstring"""

        self.device.put(self)

        return

    def start(self):
        """TODO add docstring"""

        self.device.start(self)

        return

    def free(self):
        """TODO add docstring"""

        self.device.free_sequence_bis(self)

        return
