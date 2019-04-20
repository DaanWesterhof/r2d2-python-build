from client.comm import Comm
from common.frame_enum import FrameType


class Module:
    def __init__(self):
        self.comm = Comm()
        self.comm.listen_for([FrameType.BUTTON_STATE])

    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

            print(frame)

            if frame.request:
                continue

            values = frame.get_data()

            print(values)

    def stop(self):
        self.comm.stop()