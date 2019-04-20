from client.comm import Comm
from common.frame_enum import FrameType
from common.frames import FrameButtonState


class Module:
    def __init__(self):
        self.comm = Comm()
        self.comm.listen_for([FrameType.BUTTON_STATE])

    def process(self):
        value = input("Send packet (y/n)?") == 'y'

        frame = FrameButtonState()
        frame.set_data(value)

        self.comm.send(frame)

        while self.comm.has_data():
            frame = self.comm.get_data()

            print(frame)

            if not frame.request:
                continue

    def stop(self):
        self.comm.stop()
