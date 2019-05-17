"""this file defines the module class for button_module"""

from client.comm import BaseComm
from common.frame_enum import FrameType
from common.frames import FrameButtonState


class Module:
    """this Module listens for button requests and responds with the state of the button"""
    def __init__(self, comm: BaseComm, button):
        self.comm = comm
        self.comm.listen_for([FrameType.BUTTON_STATE])
        self.button = button

    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

            if not frame.request:
                continue

            frame = FrameButtonState()
            frame["pressed"] = self.button.read()
            self.comm.send(frame)

    def stop(self):
        self.comm.stop()
