from .common import FrameType, Frame
import struct


class FrameButtonState(Frame):
    def __init__(self):
        super(FrameButtonState, self).__init__()

        self.type = FrameType.BUTTON_STATE
        self.format = '?'

    def set_data(self, state):
        self.data = struct.pack(self.format, state)


class FrameActivityLedState(Frame):
    def __init__(self):
        super(FrameActivityLedState, self).__init__()

        self.type = FrameType.ACTIVITY_LED_STATE
        self.format = '?'

    def set_data(self, state):
        self.data = struct.pack(self.format, state)


class FrameDistance(Frame):
    def __init__(self):
        super(FrameDistance, self).__init__()

        self.type = FrameType.DISTANCE
        self.format = 'H'

    def set_data(self, mm):
        self.data = struct.pack(self.format, mm)


class FrameDisplayFilledRectangle(Frame):
    def __init__(self):
        super(FrameDisplayFilledRectangle, self).__init__()

        self.type = FrameType.DISPLAY_FILLED_RECTANGLE
        self.format = 'BBBBBBB'  # 7 bytes

    def set_data(self, x, y, width, height, red, green, blue):
        self.data = struct.pack(self.format, x, y, width, height, red, green, blue)
