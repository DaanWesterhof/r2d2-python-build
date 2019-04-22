from client.comm import Comm
from common.frame_enum import FrameType
from common.frames import FrameButtonState


class Module:
    def __init__(self, button):
        self.comm = Comm()
        self.comm.listen_for([FrameType.BUTTON_STATE])
        self.button = button

    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

            if not frame.request:
                continue

            frame = FrameButtonState()
            frame.set_data(self.button.read())
            self.comm.send(frame)

    def stop(self):
        self.comm.stop()
