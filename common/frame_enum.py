#! python

""" this generated file defines Frames

it is based on the definitons of https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_types.hpp

if you have a question or a problem.
please make a github issue on https://github.com/R2D2-2019/r2d2-python-build/issues/new
or look at https://github.com/R2D2-2019/r2d2-python-build#faq
"""

from common.common import AutoNumber

__maintainer__ = "Isha Geurtsen"
__date__ = "2019-05-22 00:39:32.590335"
__status__ = "Production"
class FrameType(AutoNumber):
    NONE = ()
    BUTTON_STATE = ()
    ACTIVITY_LED_STATE = ()
    DISTANCE = ()
    DISPLAY_FILLED_RECTANGLE = ()
    DISPLAY_8X8_CHARACTER = ()
    DISPLAY_8X8_CHARACTER_VIA_CURSOR = ()
    CURSOR_POSITION = ()
    CURSOR_COLOR = ()
    BATTERY_LEVEL = ()
    UI_COMMAND = ()
    MANUAL_CONTROL = ()
    MOVEMENT_CONTROL = ()
    COORDINATE = ()
    PATH_STEP = ()
    COMMAND_LOG = ()
    COMMAND_STATUS_UPDATE = ()
    EXTERNAL = ()
    ALL = ()
    COUNT = ()
