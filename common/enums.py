
#! python

""" this generated file defines Frames

it is based on the definitons of https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_types.hpp

if you have a question or a problem.
please make a github issue on https://github.com/R2D2-2019/r2d2-python-build/issues/new
or look at https://github.com/R2D2-2019/r2d2-python-build#faq
"""

import enum

__maintainer__ = "Sebastiaan Saarloos"
__date__ = "2019-06-25 21:48:38.205986"
__status__ = "Production"

class gas_type(enum.Enum):
    LPG = enum.auto()
    CO = enum.auto()
    SMOKE = enum.auto()

class claimed_display_cursor(enum.Enum):
    OPEN_CURSOR = enum.auto()
    ROBOS_DISTANCE_CURSOR = enum.auto()
    ROBOS_TEMPERATURE_CURSOR = enum.auto()
    ROBOS_POWER_CURSOR = enum.auto()
    CURSORS_COUNT = enum.auto()

class end_effector_type(enum.Enum):
    CLAW = enum.auto()
    NONE = enum.auto()
