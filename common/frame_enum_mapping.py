#! python

"""
MAPPING maps FrameTypes on Frame class
eg:
frame_type = Frametype.BUTTON_STATE
MAPPING[frame_type] == FrameButtonState
"""

from common.common import Frame
import common.frames
from common.frame_enum import FrameType

MAPPING = {}

for obj_name in dir(common.frames):
    obj = getattr(common.frames, obj_name)
    if isinstance(obj, type) and issubclass(obj, Frame) and not obj is Frame:
        MAPPING[obj().type] = obj
