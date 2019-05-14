# this class was generated by Nicky's script on 2019-05-14 21:42:51.995649

from .common import Frame
from common.frame_enum import FrameType
import struct


class FrameButtonState(Frame):
    MEMBERS = ['pressed']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameButtonState, self).__init__()
        self.type = FrameType.BUTTON_STATE
        self.format = '?'
        self.length = 1

    def set_data(self, pressed: bool):
        self.data = struct.pack(self.format, pressed)


class FrameActivityLedState(Frame):
    MEMBERS = ['state']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameActivityLedState, self).__init__()
        self.type = FrameType.ACTIVITY_LED_STATE
        self.format = '?'
        self.length = 1

    def set_data(self, state: bool):
        self.data = struct.pack(self.format, state)


class FrameDistance(Frame):
    MEMBERS = ['mm']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDistance, self).__init__()
        self.type = FrameType.DISTANCE
        self.format = 'H'
        self.length = 2

    def set_data(self, mm: int):
        self.data = struct.pack(self.format, mm)


class FrameDisplayFilledRectangle(Frame):
    MEMBERS = ['x', 'y', 'width', 'height', 'red', 'green', 'blue']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDisplayFilledRectangle, self).__init__()
        self.type = FrameType.DISPLAY_FILLED_RECTANGLE
        self.format = 'BBBBBBB'
        self.length = 7

    def set_data(self, x: int, y: int, width: int, height: int, red: int, green: int, blue: int):
        self.data = struct.pack(self.format, x, y, width, height, red, green, blue)


class FrameUiCommand(Frame):
    MEMBERS = ['module', 'command', 'destination']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameUiCommand, self).__init__()
        self.type = FrameType.UI_COMMAND
        self.format = 'ccc'
        self.length = 3

    def set_data(self, module: str, command: str, destination: str):
        self.data = struct.pack(self.format, module, command, destination)


class FrameBatteryLevel(Frame):
    MEMBERS = ['percentage', 'voltage']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameBatteryLevel, self).__init__()
        self.type = FrameType.BATTERY_LEVEL
        self.format = 'BI'
        self.length = 5

    def set_data(self, percentage: int, voltage: int):
        self.data = struct.pack(self.format, percentage, voltage)


class FrameMovementControl(Frame):
    MEMBERS = ['speed', 'rotation', 'brake']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameMovementControl, self).__init__()
        self.type = FrameType.MOVEMENT_CONTROL
        self.format = 'cc?'
        self.length = 3

    def set_data(self, speed: int, rotation: int, brake: bool):
        self.data = struct.pack(self.format, speed, rotation, brake)


