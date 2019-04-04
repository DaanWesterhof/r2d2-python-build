import struct
from enum import Enum


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

    def set_data(self, data):
        self.data = struct.pack(data, 'HHL')
