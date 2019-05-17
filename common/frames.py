# this class was generated by Nicky's script on 2019-05-17 23:29:21.943191

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


class FrameDisplay8x8Character(Frame):
    MEMBERS = ['x', 'y', 'red', 'green', 'blue', 'characters[243]']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDisplay8x8Character, self).__init__()
        self.type = FrameType.DISPLAY_8X8_CHARACTER
        self.format = 'BBBBBc'
        self.length = 6

    def set_data(self, x: int, y: int, red: int, green: int, blue: int, characters[243]: str):
        self.data = struct.pack(self.format, x, y, red, green, blue, characters[243])


class FrameDisplay8x8CharacterViaCursor(Frame):
    MEMBERS = ['cursor_id', 'characters[247]']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDisplay8x8CharacterViaCursor, self).__init__()
        self.type = FrameType.DISPLAY_8X8_CHARACTER_VIA_CURSOR
        self.format = 'Bc'
        self.length = 2

    def set_data(self, cursor_id: int, characters[247]: str):
        self.data = struct.pack(self.format, cursor_id, characters[247])


class FrameCursorPosition(Frame):
    MEMBERS = ['cursor_id', 'cursor_x', 'cursor_y']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameCursorPosition, self).__init__()
        self.type = FrameType.CURSOR_POSITION
        self.format = 'BBB'
        self.length = 3

    def set_data(self, cursor_id: int, cursor_x: int, cursor_y: int):
        self.data = struct.pack(self.format, cursor_id, cursor_x, cursor_y)


class FrameCursorColor(Frame):
    MEMBERS = ['cursor_id', 'red', 'green', 'blue']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameCursorColor, self).__init__()
        self.type = FrameType.CURSOR_COLOR
        self.format = 'BBBB'
        self.length = 4

    def set_data(self, cursor_id: int, red: int, green: int, blue: int):
        self.data = struct.pack(self.format, cursor_id, red, green, blue)


class FrameUiCommand(Frame):
    MEMBERS = ['command', 'params', 'destination']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameUiCommand, self).__init__()
        self.type = FrameType.UI_COMMAND
        self.format = 'ccc'
        self.length = 3

    def set_data(self, command: str, params: str, destination: str):
        self.data = struct.pack(self.format, command, params, destination)


class FrameBatteryLevel(Frame):
    MEMBERS = ['voltage', 'percentage']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameBatteryLevel, self).__init__()
        self.type = FrameType.BATTERY_LEVEL
        self.format = 'IB'
        self.length = 5

    def set_data(self, voltage: int, percentage: int):
        self.data = struct.pack(self.format, voltage, percentage)


class FrameManualControl(Frame):
    MEMBERS = ['speed', 'rotation', 'brake']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameManualControl, self).__init__()
        self.type = FrameType.MANUAL_CONTROL
        self.format = 'cc?'
        self.length = 3

    def set_data(self, speed: int, rotation: int, brake: bool):
        self.data = struct.pack(self.format, speed, rotation, brake)


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


class FramePathStep(Frame):
    MEMBERS = ['x', 'y', 'step_id', 'path_id']
    DESCRIPTION = ""

    def __init__(self):
        super(FramePathStep, self).__init__()
        self.type = FrameType.PATH_STEP
        self.format = 'IIHB'
        self.length = 11

    def set_data(self, x: int, y: int, step_id: int, path_id: int):
        self.data = struct.pack(self.format, x, y, step_id, path_id)


class FrameCommandLog(Frame):
    MEMBERS = ['status', 'original_command', 'original_data']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameCommandLog, self).__init__()
        self.type = FrameType.COMMAND_LOG
        self.format = 'Hcc'
        self.length = 4

    def set_data(self, status: int, original_command: str, original_data: str):
        self.data = struct.pack(self.format, status, original_command, original_data)


class FrameCommandStatusUpdate(Frame):
    MEMBERS = ['cmd_id', 'status']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameCommandStatusUpdate, self).__init__()
        self.type = FrameType.COMMAND_STATUS_UPDATE
        self.format = 'IH'
        self.length = 6

    def set_data(self, cmd_id: int, status: int):
        self.data = struct.pack(self.format, cmd_id, status)


