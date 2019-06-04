
#! python
""" this generated file defines Frames

it is based on the definitons of https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_types.hpp

if you have a question or a problem.
please make a github issue on https://github.com/R2D2-2019/r2d2-python-build/issues/new
or look at https://github.com/R2D2-2019/r2d2-python-build#faq
"""

from common.common import AutoNumber

__maintainer__ = "Sebastiaan Saarloos"
__date__ = "2019-06-04 17:09:01.153106"
__status__ = "Production"

class gas_type(AutoNumber): 
    LPG = ()
    CO = ()
    SMOKE = ()

class claimed_display_cursor(AutoNumber): 
    OPEN_CURSOR = ()
    ROBOS_DISTANCE_CURSOR = ()
    ROBOS_TEMPERATURE_CURSOR = ()
    ROBOS_POWER_CURSOR = ()
    CURSORS_COUNT = ()

class end_effector_type(AutoNumber): 
    CLAW = ()
    NONE = ()

