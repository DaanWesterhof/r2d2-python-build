#! python

""" this generated file defines Frames

it is based on the definitons of https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_types.hpp

if you have a question or a problem.
please make a github issue on https://github.com/R2D2-2019/r2d2-python-build/issues/new
or look at https://github.com/R2D2-2019/r2d2-python-build#faq
"""

import struct
from .common import Frame
from common.frame_enum import FrameType

__maintainer__ = "Isha Geurtsen"
__date__ = "2019-06-28 13:33:17.310247"
__status__ = "Production"
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


class FrameDisplayRectangle(Frame):
    MEMBERS = ['x', 'y', 'width', 'height', 'filled', 'red', 'green', 'blue']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDisplayRectangle, self).__init__()
        self.type = FrameType.DISPLAY_RECTANGLE
        self.format = 'B B B B ? B B B'
        self.length = 8

    def set_data(self, x: int, y: int, width: int, height: int, filled: bool, red: int, green: int, blue: int):
        self.data = struct.pack(self.format, x, y, width, height, filled, red, green, blue)


class FrameDisplayRectangleViaCursor(Frame):
    MEMBERS = ['cursor_id', 'width', 'height', 'filled', 'red', 'green', 'blue']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDisplayRectangleViaCursor, self).__init__()
        self.type = FrameType.DISPLAY_RECTANGLE_VIA_CURSOR
        self.format = 'B B B ? B B B'
        self.length = 7

    def set_data(self, cursor_id: int, width: int, height: int, filled: bool, red: int, green: int, blue: int):
        self.data = struct.pack(self.format, cursor_id, width, height, filled, red, green, blue)


class FrameDisplay8x8Character(Frame):
    MEMBERS = ['x', 'y', 'red', 'green', 'blue', 'characters']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDisplay8x8Character, self).__init__()
        self.type = FrameType.DISPLAY_8X8_CHARACTER
        self.format = 'B B B B B 243s'
        self.length = 248

    def set_data(self, x: int, y: int, red: int, green: int, blue: int, characters: str):
        self.data = struct.pack(self.format, x, y, red, green, blue, characters)


class FrameDisplay8x8CharacterViaCursor(Frame):
    MEMBERS = ['cursor_id', 'characters']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDisplay8x8CharacterViaCursor, self).__init__()
        self.type = FrameType.DISPLAY_8X8_CHARACTER_VIA_CURSOR
        self.format = 'B 247s'
        self.length = 248

    def set_data(self, cursor_id: int, characters: str):
        self.data = struct.pack(self.format, cursor_id, characters)


class FrameDisplayCircle(Frame):
    MEMBERS = ['x', 'y', 'radius', 'filled', 'red', 'green', 'blue']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDisplayCircle, self).__init__()
        self.type = FrameType.DISPLAY_CIRCLE
        self.format = 'B B B ? B B B'
        self.length = 7

    def set_data(self, x: int, y: int, radius: int, filled: bool, red: int, green: int, blue: int):
        self.data = struct.pack(self.format, x, y, radius, filled, red, green, blue)


class FrameDisplayCircleViaCursor(Frame):
    MEMBERS = ['cursor_id', 'radius', 'filled', 'red', 'green', 'blue']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDisplayCircleViaCursor, self).__init__()
        self.type = FrameType.DISPLAY_CIRCLE_VIA_CURSOR
        self.format = 'B B ? B B B'
        self.length = 6

    def set_data(self, cursor_id: int, radius: int, filled: bool, red: int, green: int, blue: int):
        self.data = struct.pack(self.format, cursor_id, radius, filled, red, green, blue)


class FrameCursorPosition(Frame):
    MEMBERS = ['cursor_id', 'cursor_x', 'cursor_y']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameCursorPosition, self).__init__()
        self.type = FrameType.CURSOR_POSITION
        self.format = 'B B B'
        self.length = 3

    def set_data(self, cursor_id: int, cursor_x: int, cursor_y: int):
        self.data = struct.pack(self.format, cursor_id, cursor_x, cursor_y)


class FrameCursorColor(Frame):
    MEMBERS = ['cursor_id', 'red', 'green', 'blue']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameCursorColor, self).__init__()
        self.type = FrameType.CURSOR_COLOR
        self.format = 'B B B B'
        self.length = 4

    def set_data(self, cursor_id: int, red: int, green: int, blue: int):
        self.data = struct.pack(self.format, cursor_id, red, green, blue)


class FrameTemperature(Frame):
    MEMBERS = ['id', 'ambient_temperature', 'object_temperature']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameTemperature, self).__init__()
        self.type = FrameType.TEMPERATURE
        self.format = 'I h h'
        self.length = 8

    def set_data(self, id: int, ambient_temperature: int, object_temperature: int):
        self.data = struct.pack(self.format, id, ambient_temperature, object_temperature)


class FrameUiCommand(Frame):
    MEMBERS = ['command', 'params', 'destination']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameUiCommand, self).__init__()
        self.type = FrameType.UI_COMMAND
        self.format = 'c c c'
        self.length = 3

    def set_data(self, command: str, params: str, destination: str):
        self.data = struct.pack(self.format, command, params, destination)


class FrameRobotNames(Frame):
    MEMBERS = ['names']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameRobotNames, self).__init__()
        self.type = FrameType.ROBOT_NAMES
        self.format = 'c'
        self.length = 1

    def set_data(self, names: str):
        self.data = struct.pack(self.format, names)


class FrameSwarmNames(Frame):
    MEMBERS = ['names']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameSwarmNames, self).__init__()
        self.type = FrameType.SWARM_NAMES
        self.format = 'c'
        self.length = 1

    def set_data(self, names: str):
        self.data = struct.pack(self.format, names)


class FrameBatteryLevel(Frame):
    MEMBERS = ['voltage', 'percentage']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameBatteryLevel, self).__init__()
        self.type = FrameType.BATTERY_LEVEL
        self.format = 'I B'
        self.length = 5

    def set_data(self, voltage: int, percentage: int):
        self.data = struct.pack(self.format, voltage, percentage)


class FrameManualControl(Frame):
    MEMBERS = ['speed', 'rotation', 'brake']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameManualControl, self).__init__()
        self.type = FrameType.MANUAL_CONTROL
        self.format = 'b b ?'
        self.length = 3

    def set_data(self, speed: int, rotation: int, brake: bool):
        self.data = struct.pack(self.format, speed, rotation, brake)


class FrameManualControlButton(Frame):
    MEMBERS = ['controller_id', 'button_id', 'value']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameManualControlButton, self).__init__()
        self.type = FrameType.MANUAL_CONTROL_BUTTON
        self.format = 'B B ?'
        self.length = 3

    def set_data(self, controller_id: int, button_id: int, value: bool):
        self.data = struct.pack(self.format, controller_id, button_id, value)


class FrameManualControlSlider(Frame):
    MEMBERS = ['controller_id', 'slider_id', 'value']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameManualControlSlider, self).__init__()
        self.type = FrameType.MANUAL_CONTROL_SLIDER
        self.format = 'B B B'
        self.length = 3

    def set_data(self, controller_id: int, slider_id: int, value: int):
        self.data = struct.pack(self.format, controller_id, slider_id, value)


class FrameManualControlJoystick(Frame):
    MEMBERS = ['controller_id', 'joystick_id', 'value_x', 'value_y']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameManualControlJoystick, self).__init__()
        self.type = FrameType.MANUAL_CONTROL_JOYSTICK
        self.format = 'B B b b'
        self.length = 4

    def set_data(self, controller_id: int, joystick_id: int, value_x: int, value_y: int):
        self.data = struct.pack(self.format, controller_id, joystick_id, value_x, value_y)


class FrameMovementControl(Frame):
    MEMBERS = ['speed', 'rotation', 'brake']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameMovementControl, self).__init__()
        self.type = FrameType.MOVEMENT_CONTROL
        self.format = 'b b ?'
        self.length = 3

    def set_data(self, speed: int, rotation: int, brake: bool):
        self.data = struct.pack(self.format, speed, rotation, brake)


class FrameCoordinate(Frame):
    MEMBERS = ['altitude', 'long_tenthousandth_min', 'lat_tenthousandth_min', 'lat_deg', 'lat_min', 'long_deg', 'long_min', 'north_south_hemisphere', 'east_west_hemisphere']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameCoordinate, self).__init__()
        self.type = FrameType.COORDINATE
        self.format = 'h H H B B B B ? ?'
        self.length = 12

    def set_data(self, altitude: int, long_tenthousandth_min: int, lat_tenthousandth_min: int, lat_deg: int, lat_min: int, long_deg: int, long_min: int, north_south_hemisphere: bool, east_west_hemisphere: bool):
        self.data = struct.pack(self.format, altitude, long_tenthousandth_min, lat_tenthousandth_min, lat_deg, lat_min, long_deg, long_min, north_south_hemisphere, east_west_hemisphere)


class FramePathStep(Frame):
    MEMBERS = ['x', 'y', 'step_id', 'path_id']
    DESCRIPTION = ""

    def __init__(self):
        super(FramePathStep, self).__init__()
        self.type = FrameType.PATH_STEP
        self.format = 'I I H B'
        self.length = 11

    def set_data(self, x: int, y: int, step_id: int, path_id: int):
        self.data = struct.pack(self.format, x, y, step_id, path_id)


class FrameMicrophone(Frame):
    MEMBERS = ['length', 'microphone_data']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameMicrophone, self).__init__()
        self.type = FrameType.MICROPHONE
        self.format = 'B h'
        self.length = 3

    def set_data(self, length: int, microphone_data: int):
        self.data = struct.pack(self.format, length, microphone_data)


class FrameCommandLog(Frame):
    MEMBERS = ['status', 'original_command', 'original_data']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameCommandLog, self).__init__()
        self.type = FrameType.COMMAND_LOG
        self.format = 'H c c'
        self.length = 4

    def set_data(self, status: int, original_command: str, original_data: str):
        self.data = struct.pack(self.format, status, original_command, original_data)


class FrameCommandStatusUpdate(Frame):
    MEMBERS = ['cmd_id', 'status']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameCommandStatusUpdate, self).__init__()
        self.type = FrameType.COMMAND_STATUS_UPDATE
        self.format = 'I H'
        self.length = 6

    def set_data(self, cmd_id: int, status: int):
        self.data = struct.pack(self.format, cmd_id, status)


class FrameCommandId(Frame):
    MEMBERS = ['command_id']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameCommandId, self).__init__()
        self.type = FrameType.COMMAND_ID
        self.format = 'I'
        self.length = 4

    def set_data(self, command_id: int):
        self.data = struct.pack(self.format, command_id)


class FrameGas(Frame):
    MEMBERS = ['gas_value', 'gas_id']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameGas, self).__init__()
        self.type = FrameType.GAS
        self.format = 'H B'
        self.length = 3

    def set_data(self, gas_value: int, gas_id: int):
        self.data = struct.pack(self.format, gas_value, gas_id)


class FrameRtttlString(Frame):
    MEMBERS = ['rtttl_string']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameRtttlString, self).__init__()
        self.type = FrameType.RTTTL_STRING
        self.format = '248s'
        self.length = 248

    def set_data(self, rtttl_string: str):
        self.data = struct.pack(self.format, rtttl_string)


class FrameRequestMapObstacles(Frame):
    MEMBERS = ['path_id']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameRequestMapObstacles, self).__init__()
        self.type = FrameType.REQUEST_MAP_OBSTACLES
        self.format = 'B'
        self.length = 1

    def set_data(self, path_id: int):
        self.data = struct.pack(self.format, path_id)


class FrameMapInfo(Frame):
    MEMBERS = ['obstacle_count', 'width', 'height', 'path_id', 'map_id']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameMapInfo, self).__init__()
        self.type = FrameType.MAP_INFO
        self.format = 'H H H B B'
        self.length = 8

    def set_data(self, obstacle_count: int, width: int, height: int, path_id: int, map_id: int):
        self.data = struct.pack(self.format, obstacle_count, width, height, path_id, map_id)


class FrameMapObstacle(Frame):
    MEMBERS = ['x', 'y', 'map_id']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameMapObstacle, self).__init__()
        self.type = FrameType.MAP_OBSTACLE
        self.format = 'H H B'
        self.length = 5

    def set_data(self, x: int, y: int, map_id: int):
        self.data = struct.pack(self.format, x, y, map_id)


class FrameEndEffectorType(Frame):
    MEMBERS = ['type']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameEndEffectorType, self).__init__()
        self.type = FrameType.END_EFFECTOR_TYPE
        self.format = 'B'
        self.length = 1

    def set_data(self, type: int):
        self.data = struct.pack(self.format, type)


class FrameEndEffectorClaw(Frame):
    MEMBERS = ['close']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameEndEffectorClaw, self).__init__()
        self.type = FrameType.END_EFFECTOR_CLAW
        self.format = '?'
        self.length = 1

    def set_data(self, close: bool):
        self.data = struct.pack(self.format, close)


class FrameFlameDetection(Frame):
    MEMBERS = ['flame_detected', 'big_fire', 'flame_angle']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameFlameDetection, self).__init__()
        self.type = FrameType.FLAME_DETECTION
        self.format = '? ? i'
        self.length = 6

    def set_data(self, flame_detected: bool, big_fire: bool, flame_angle: int):
        self.data = struct.pack(self.format, flame_detected, big_fire, flame_angle)


class FrameQrcodeData(Frame):
    MEMBERS = ['message', 'width', 'height', 'x_offset', 'y_offset', 'distance_in_mm']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameQrcodeData, self).__init__()
        self.type = FrameType.QRCODE_DATA
        self.format = 'c H H H H H'
        self.length = 11

    def set_data(self, message: str, width: int, height: int, x_offset: int, y_offset: int, distance_in_mm: int):
        self.data = struct.pack(self.format, message, width, height, x_offset, y_offset, distance_in_mm)


