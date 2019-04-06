from client.comm import Comm
from common.common import FrameType


class Module:
    def __init__(self):
        self.comm = Comm()

    def process(self):
        self.comm.send(FrameType.BUTTON_STATE, (1,2,3))

        while self.comm.has_data():
            print(self.comm.get_data())
            print()
