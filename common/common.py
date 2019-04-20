import struct
from enum import Enum


class BusConfig:
    AUTH_KEY = b'r2d2'
    PORT = 5000
    ADDRESS = ('127.0.0.1', PORT)


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__)  # note no + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class Priority(Enum):
    HIGH = 0
    NORMAL = 1
    LOW = 2
    DATA_STREAM = 3


class Frame:
    def __init__(self):
        # Set in child class
        self.format = ''

        self.type = None
        self.data = None
        self.length = 0
        self.request = False
        self.priority = Priority.NORMAL

    def __str__(self):
        return "Type: {}\nData: bytes\nLength: {}\nRequest: {}".format(
            self.type,
            self.length,
            self.request
        )

    def set_data(self, data):
        pass

    def get_data(self):
        return struct.unpack(self.format, self.data)


class FrameWrapper:
    def __init__(self, frame, pid, timestamp):
        self.frame = frame
        self.pid = pid
        self.timestamp = timestamp