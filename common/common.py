import struct
from enum import Enum


class Priority(Enum):
    HIGH = 0
    NORMAL = 1
    LOW = 2
    DATA_STREAM = 3


class FrameType(Enum):
    NONE = 0

    BUTTON_STATE = 1
    ACTIVITY_LED_STATE = 2
    DISTANCE = 3

    EXTERNAL = 4
    ALL = 5
    COUNT = 6


class Frame:
    def __init__(self):
        self.type = None
        self.data = bytearray(8)
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
        self.data = struct.pack(data, 'HHL')
