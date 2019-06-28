#! python

""" this generated file defines Frames

it is based on the definitons of https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_types.hpp

if you have a question or a problem.
please make a github issue on https://github.com/R2D2-2019/r2d2-python-build/issues/new
or look at https://github.com/R2D2-2019/r2d2-python-build#faq
"""

from common.common import AutoNumber

__maintainer__ = "Isha Geurtsen"
__date__ = "2019-06-28 18:36:07.172051"
__status__ = "Production"
class FrameType(AutoNumber):
    NONE = ()
    BUTTON_STATE = ()
    ACTIVITY_LED_STATE = ()
    DISTANCE = ()
    DISPLAY_RECTANGLE = ()
    DISPLAY_RECTANGLE_VIA_CURSOR = ()
    DISPLAY_8X8_CHARACTER = ()
    DISPLAY_8X8_CHARACTER_VIA_CURSOR = ()
    DISPLAY_CIRCLE = ()
    DISPLAY_CIRCLE_VIA_CURSOR = ()
    CURSOR_POSITION = ()
    CURSOR_COLOR = ()
    UI_COMMAND = ()
    ROBOT_NAMES = ()
    SWARM_NAMES = ()
    BATTERY_LEVEL = ()
    MANUAL_CONTROL = ()
    MANUAL_CONTROL_BUTTON = ()
    MANUAL_CONTROL_SLIDER = ()
    MANUAL_CONTROL_JOYSTICK = ()
    MICROPHONE = ()
    MOVEMENT_CONTROL = ()
    COORDINATE = ()
    PATH_STEP = ()
    COMMAND_LOG = ()
    COMMAND_STATUS_UPDATE = ()
    COMMAND_ID = ()
    TEMPERATURE = ()
    GAS = ()
    QRCODE_DATA = ()
    RTTTL_STRING = ()
    REQUEST_MAP_OBSTACLES = ()
    MAP_INFO = ()
    MAP_OBSTACLE = ()
    END_EFFECTOR_TYPE = ()
    END_EFFECTOR_CLAW = ()
    FLAME_DETECTION = ()
    EXTERNAL = ()
    ALL = ()
    COUNT = ()
