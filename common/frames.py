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
__date__ = "2019-06-28 22:19:17.913888"
__status__ = "Production"
class FrameButtonState(Frame):
    MEMBERS = ['pressed']
    DESCRIPTION = ""
    __annotations__ = {'pressed':bool}

    def __init__(self):
        super(FrameButtonState, self).__init__()
        self.type = FrameType.BUTTON_STATE
        self.format = '?'
        self.length = 1

class FrameActivityLedState(Frame):
    MEMBERS = ['state']
    DESCRIPTION = ""
    __annotations__ = {'state':bool}

    def __init__(self):
        super(FrameActivityLedState, self).__init__()
        self.type = FrameType.ACTIVITY_LED_STATE
        self.format = '?'
        self.length = 1

class FrameDistance(Frame):
    MEMBERS = ['mm']
    DESCRIPTION = ""
    __annotations__ = {'mm':int}

    def __init__(self):
        super(FrameDistance, self).__init__()
        self.type = FrameType.DISTANCE
        self.format = 'H'
        self.length = 2

class FrameDisplayRectangle(Frame):
    MEMBERS = ['x', 'y', 'width', 'height', 'filled', 'red', 'green', 'blue']
    DESCRIPTION = ""
    __annotations__ = {'x':int, 'y':int, 'width':int, 'height':int, 'filled':bool, 'red':int, 'green':int, 'blue':int}

    def __init__(self):
        super(FrameDisplayRectangle, self).__init__()
        self.type = FrameType.DISPLAY_RECTANGLE
        self.format = 'B B B B ? B B B'
        self.length = 8

class FrameDisplayRectangleViaCursor(Frame):
    MEMBERS = ['cursor_id', 'width', 'height', 'filled', 'red', 'green', 'blue']
    DESCRIPTION = ""
    __annotations__ = {'cursor_id':int, 'width':int, 'height':int, 'filled':bool, 'red':int, 'green':int, 'blue':int}

    def __init__(self):
        super(FrameDisplayRectangleViaCursor, self).__init__()
        self.type = FrameType.DISPLAY_RECTANGLE_VIA_CURSOR
        self.format = 'B B B ? B B B'
        self.length = 7

class FrameDisplay8x8Character(Frame):
    MEMBERS = ['x', 'y', 'red', 'green', 'blue', 'characters']
    DESCRIPTION = ""
    __annotations__ = {'x':int, 'y':int, 'red':int, 'green':int, 'blue':int, 'characters':str}

    def __init__(self):
        super(FrameDisplay8x8Character, self).__init__()
        self.type = FrameType.DISPLAY_8X8_CHARACTER
        self.format = 'B B B B B 243s'
        self.length = 248

class FrameDisplay8x8CharacterViaCursor(Frame):
    MEMBERS = ['cursor_id', 'characters']
    DESCRIPTION = ""
    __annotations__ = {'cursor_id':int, 'characters':str}

    def __init__(self):
        super(FrameDisplay8x8CharacterViaCursor, self).__init__()
        self.type = FrameType.DISPLAY_8X8_CHARACTER_VIA_CURSOR
        self.format = 'B 247s'
        self.length = 248

class FrameDisplayCircle(Frame):
    MEMBERS = ['x', 'y', 'radius', 'filled', 'red', 'green', 'blue']
    DESCRIPTION = ""
    __annotations__ = {'x':int, 'y':int, 'radius':int, 'filled':bool, 'red':int, 'green':int, 'blue':int}

    def __init__(self):
        super(FrameDisplayCircle, self).__init__()
        self.type = FrameType.DISPLAY_CIRCLE
        self.format = 'B B B ? B B B'
        self.length = 7

class FrameDisplayCircleViaCursor(Frame):
    MEMBERS = ['cursor_id', 'radius', 'filled', 'red', 'green', 'blue']
    DESCRIPTION = ""
    __annotations__ = {'cursor_id':int, 'radius':int, 'filled':bool, 'red':int, 'green':int, 'blue':int}

    def __init__(self):
        super(FrameDisplayCircleViaCursor, self).__init__()
        self.type = FrameType.DISPLAY_CIRCLE_VIA_CURSOR
        self.format = 'B B ? B B B'
        self.length = 6

class FrameCursorPosition(Frame):
    MEMBERS = ['cursor_id', 'cursor_x', 'cursor_y']
    DESCRIPTION = ""
    __annotations__ = {'cursor_id':int, 'cursor_x':int, 'cursor_y':int}

    def __init__(self):
        super(FrameCursorPosition, self).__init__()
        self.type = FrameType.CURSOR_POSITION
        self.format = 'B B B'
        self.length = 3

class FrameCursorColor(Frame):
    MEMBERS = ['cursor_id', 'red', 'green', 'blue']
    DESCRIPTION = ""
    __annotations__ = {'cursor_id':int, 'red':int, 'green':int, 'blue':int}

    def __init__(self):
        super(FrameCursorColor, self).__init__()
        self.type = FrameType.CURSOR_COLOR
        self.format = 'B B B B'
        self.length = 4

class FrameTemperature(Frame):
    MEMBERS = ['id', 'ambient_temperature', 'object_temperature']
    DESCRIPTION = ""
    __annotations__ = {'id':int, 'ambient_temperature':int, 'object_temperature':int}

    def __init__(self):
        super(FrameTemperature, self).__init__()
        self.type = FrameType.TEMPERATURE
        self.format = 'I h h'
        self.length = 8

class FrameUiCommand(Frame):
    MEMBERS = ['command', 'params', 'destination']
    DESCRIPTION = ""
    __annotations__ = {'command':str, 'params':str, 'destination':str}

    def __init__(self):
        super(FrameUiCommand, self).__init__()
        self.type = FrameType.UI_COMMAND
        self.format = 'c c c'
        self.length = 3

class FrameRobotNames(Frame):
    MEMBERS = ['names']
    DESCRIPTION = ""
    __annotations__ = {'names':str}

    def __init__(self):
        super(FrameRobotNames, self).__init__()
        self.type = FrameType.ROBOT_NAMES
        self.format = 'c'
        self.length = 1

class FrameSwarmNames(Frame):
    MEMBERS = ['names']
    DESCRIPTION = ""
    __annotations__ = {'names':str}

    def __init__(self):
        super(FrameSwarmNames, self).__init__()
        self.type = FrameType.SWARM_NAMES
        self.format = 'c'
        self.length = 1

class FrameBatteryLevel(Frame):
    MEMBERS = ['voltage', 'percentage']
    DESCRIPTION = ""
    __annotations__ = {'voltage':int, 'percentage':int}

    def __init__(self):
        super(FrameBatteryLevel, self).__init__()
        self.type = FrameType.BATTERY_LEVEL
        self.format = 'I B'
        self.length = 5

class FrameManualControl(Frame):
    MEMBERS = ['speed', 'rotation', 'brake']
    DESCRIPTION = ""
    __annotations__ = {'speed':int, 'rotation':int, 'brake':bool}

    def __init__(self):
        super(FrameManualControl, self).__init__()
        self.type = FrameType.MANUAL_CONTROL
        self.format = 'b b ?'
        self.length = 3

class FrameManualControlButton(Frame):
    MEMBERS = ['controller_id', 'button_id', 'value']
    DESCRIPTION = ""
    __annotations__ = {'controller_id':int, 'button_id':int, 'value':bool}

    def __init__(self):
        super(FrameManualControlButton, self).__init__()
        self.type = FrameType.MANUAL_CONTROL_BUTTON
        self.format = 'B B ?'
        self.length = 3

class FrameManualControlSlider(Frame):
    MEMBERS = ['controller_id', 'slider_id', 'value']
    DESCRIPTION = ""
    __annotations__ = {'controller_id':int, 'slider_id':int, 'value':int}

    def __init__(self):
        super(FrameManualControlSlider, self).__init__()
        self.type = FrameType.MANUAL_CONTROL_SLIDER
        self.format = 'B B B'
        self.length = 3

class FrameManualControlJoystick(Frame):
    MEMBERS = ['controller_id', 'joystick_id', 'value_x', 'value_y']
    DESCRIPTION = ""
    __annotations__ = {'controller_id':int, 'joystick_id':int, 'value_x':int, 'value_y':int}

    def __init__(self):
        super(FrameManualControlJoystick, self).__init__()
        self.type = FrameType.MANUAL_CONTROL_JOYSTICK
        self.format = 'B B b b'
        self.length = 4

class FrameMovementControl(Frame):
    MEMBERS = ['speed', 'rotation', 'brake']
    DESCRIPTION = ""
    __annotations__ = {'speed':int, 'rotation':int, 'brake':bool}

    def __init__(self):
        super(FrameMovementControl, self).__init__()
        self.type = FrameType.MOVEMENT_CONTROL
        self.format = 'b b ?'
        self.length = 3

class FrameCoordinate(Frame):
    MEMBERS = ['altitude', 'long_tenthousandth_min', 'lat_tenthousandth_min', 'lat_deg', 'lat_min', 'long_deg', 'long_min', 'north_south_hemisphere', 'east_west_hemisphere']
    DESCRIPTION = ""
    __annotations__ = {'altitude':int, 'long_tenthousandth_min':int, 'lat_tenthousandth_min':int, 'lat_deg':int, 'lat_min':int, 'long_deg':int, 'long_min':int, 'north_south_hemisphere':bool, 'east_west_hemisphere':bool}

    def __init__(self):
        super(FrameCoordinate, self).__init__()
        self.type = FrameType.COORDINATE
        self.format = 'h H H B B B B ? ?'
        self.length = 12

class FramePathStep(Frame):
    MEMBERS = ['x', 'y', 'step_id', 'path_id']
    DESCRIPTION = ""
    __annotations__ = {'x':int, 'y':int, 'step_id':int, 'path_id':int}

    def __init__(self):
        super(FramePathStep, self).__init__()
        self.type = FrameType.PATH_STEP
        self.format = 'I I H B'
        self.length = 11

class FrameMicrophone(Frame):
    MEMBERS = ['length', 'microphone_data']
    DESCRIPTION = ""
    __annotations__ = {'length':int, 'microphone_data':list}

    def __init__(self):
        super(FrameMicrophone, self).__init__()
        self.type = FrameType.MICROPHONE
        self.format = 'B 64h'
        self.length = 130

class FrameCommandLog(Frame):
    MEMBERS = ['status', 'original_command', 'original_data']
    DESCRIPTION = ""
    __annotations__ = {'status':int, 'original_command':str, 'original_data':str}

    def __init__(self):
        super(FrameCommandLog, self).__init__()
        self.type = FrameType.COMMAND_LOG
        self.format = 'H c c'
        self.length = 4

class FrameCommandStatusUpdate(Frame):
    MEMBERS = ['cmd_id', 'status']
    DESCRIPTION = ""
    __annotations__ = {'cmd_id':int, 'status':int}

    def __init__(self):
        super(FrameCommandStatusUpdate, self).__init__()
        self.type = FrameType.COMMAND_STATUS_UPDATE
        self.format = 'I H'
        self.length = 6

class FrameCommandId(Frame):
    MEMBERS = ['command_id']
    DESCRIPTION = ""
    __annotations__ = {'command_id':int}

    def __init__(self):
        super(FrameCommandId, self).__init__()
        self.type = FrameType.COMMAND_ID
        self.format = 'I'
        self.length = 4

class FrameGas(Frame):
    MEMBERS = ['gas_value', 'gas_id']
    DESCRIPTION = ""
    __annotations__ = {'gas_value':int, 'gas_id':int}

    def __init__(self):
        super(FrameGas, self).__init__()
        self.type = FrameType.GAS
        self.format = 'H B'
        self.length = 3

class FrameRtttlString(Frame):
    MEMBERS = ['rtttl_string']
    DESCRIPTION = ""
    __annotations__ = {'rtttl_string':str}

    def __init__(self):
        super(FrameRtttlString, self).__init__()
        self.type = FrameType.RTTTL_STRING
        self.format = '248s'
        self.length = 248

class FrameRequestMapObstacles(Frame):
    MEMBERS = ['path_id']
    DESCRIPTION = ""
    __annotations__ = {'path_id':int}

    def __init__(self):
        super(FrameRequestMapObstacles, self).__init__()
        self.type = FrameType.REQUEST_MAP_OBSTACLES
        self.format = 'B'
        self.length = 1

class FrameMapInfo(Frame):
    MEMBERS = ['obstacle_count', 'width', 'height', 'path_id', 'map_id']
    DESCRIPTION = ""
    __annotations__ = {'obstacle_count':int, 'width':int, 'height':int, 'path_id':int, 'map_id':int}

    def __init__(self):
        super(FrameMapInfo, self).__init__()
        self.type = FrameType.MAP_INFO
        self.format = 'H H H B B'
        self.length = 8

class FrameMapObstacle(Frame):
    MEMBERS = ['x', 'y', 'map_id']
    DESCRIPTION = ""
    __annotations__ = {'x':int, 'y':int, 'map_id':int}

    def __init__(self):
        super(FrameMapObstacle, self).__init__()
        self.type = FrameType.MAP_OBSTACLE
        self.format = 'H H B'
        self.length = 5

class FrameEndEffectorType(Frame):
    MEMBERS = ['type']
    DESCRIPTION = ""
    __annotations__ = {'type':int}

    def __init__(self):
        super(FrameEndEffectorType, self).__init__()
        self.type = FrameType.END_EFFECTOR_TYPE
        self.format = 'B'
        self.length = 1

class FrameEndEffectorClaw(Frame):
    MEMBERS = ['close']
    DESCRIPTION = ""
    __annotations__ = {'close':bool}

    def __init__(self):
        super(FrameEndEffectorClaw, self).__init__()
        self.type = FrameType.END_EFFECTOR_CLAW
        self.format = '?'
        self.length = 1

class FrameFlameDetection(Frame):
    MEMBERS = ['flame_detected', 'big_fire', 'flame_angle']
    DESCRIPTION = ""
    __annotations__ = {'flame_detected':bool, 'big_fire':bool, 'flame_angle':int}

    def __init__(self):
        super(FrameFlameDetection, self).__init__()
        self.type = FrameType.FLAME_DETECTION
        self.format = '? ? i'
        self.length = 8

class FrameQrcodeData(Frame):
    MEMBERS = ['message', 'width', 'height', 'x_offset', 'y_offset', 'distance_in_mm']
    DESCRIPTION = ""
    __annotations__ = {'message':str, 'width':int, 'height':int, 'x_offset':int, 'y_offset':int, 'distance_in_mm':int}

    def __init__(self):
        super(FrameQrcodeData, self).__init__()
        self.type = FrameType.QRCODE_DATA
        self.format = '200s H H h h H'
        self.length = 210

