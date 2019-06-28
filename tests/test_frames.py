#! python

"""this module tests the frames in common/frames.py"""

import datetime
import common.common
import common.frames
import common.frame_enum

__author__ = "Isha geurtsen"
__version__ = "0.1.0"
__maintainer__ = "Isha geurtsen"
__email__ = "isha.geurtsen@student.hu.nl"
__status__ = "Development"
__date__ = datetime.datetime(2019, 5, 21, 23, 10)

FRAMES = list(
    map(
        (lambda name: getattr(common.frames, name)),
        filter(
            (
                lambda name:
                str.startswith(name, "Frame")
                and name not in ["FrameType", "Frame"]
            ),
            dir(common.frames)
        )
    )
)


def test_frame_enum_format():
    """this test asserts that all enumerated names of FrameType are upper case"""
    for frame_type in common.frame_enum.FrameType:
        assert frame_type.name == str.upper(frame_type.name)


def test_frame_type_in_enum():
    """this test asserts that all frames have a corisponding enum"""
    for frame in FRAMES:
        assert isinstance(frame().type, common.frame_enum.FrameType)


def test_frames_isinstance_of_frame():
    """this test asserts that all frames are an instance of Frame"""
    for frame in FRAMES:
        assert issubclass(frame, common.common.Frame)


def test_frame_can_set_data():
    """
    this test asserts that all frames can be called with set_data
    """
    manual_data = {
        common.frame_enum.FrameType.MICROPHONE: (0, (0,)*64),
    }
    for frame_class in FRAMES:
        frame = frame_class()
        annotations = frame.__annotations__
        args = tuple(annotations[name]() for name in frame.MEMBERS)
        if frame.type in manual_data:
            args = manual_data[frame.type]
        frame.set_data(*args)
        assert args == frame.get_data()


def test_frame_can_set_item():
    manual_data = {
        common.frame_enum.FrameType.MICROPHONE: {
            'microphone_data': (0,)*64,
        }
    }
    for frame_class in FRAMES:
        annotations = frame_class.__annotations__
        for name in frame_class.MEMBERS:
            frame = frame_class()
            if frame.type in manual_data and name in manual_data[frame.type]:
                item = manual_data[frame.type][name]
            else:
                item = annotations[name]()
            frame[name] = item
            assert frame[name] == item
