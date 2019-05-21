#! python

""" this generated file defines Frames

it is based on the definitons of https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_types.hpp

if you have a question or a problem.
please make a github issue on https://github.com/R2D2-2019/r2d2-python-build/issues/new
or look at https://github.com/R2D2-2019/r2d2-python-build#faq
"""

from common.common import AutoNumber

__maintainer = "Isha Geurtsen"
__date__ = "2019-05-20 03:44:47.635566"
__status__ = "Production"
class FrameType(AutoNumber):
    NONE = ()
    BUTTON_STATE = ()
    ACTIVITY_LED_STATE = ()
    DISTANCE = ()
    DISPLAY_FILLED_RECTANGLE = ()
    DISPLAY_8x8_CHARACTER = ()
    DISPLAY_8x8_CURSOR_CHARACTER = ()
    CURSOR_POSITION = ()
    CURSOR_COLOR = ()
    BATTERY_LEVEL = ()
    UI_COMMAND = ()
    MANUAL_CONTROL = ()
    MOVEMENT_CONTROL = ()
    COORDINATE_STRUCT = ()
    PATH_STEP = ()
    COMMAND_LOG = ()
    COMMAND_STATUS_UPDATE = ()
    EXTERNAL = ()
    ALL = ()
    COUNT = ()
