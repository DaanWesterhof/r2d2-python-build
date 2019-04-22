from client.comm import BaseComm
from common.frame_enum import FrameType


class Module:
    def __init__(self, comm: BaseComm):
        self.comm = comm
        # self.comm.listen_for([FrameType.BUTTON_STATE])

    def process(self):
        # self.comm.send(FrameType.BUTTON_STATE, (1,2,3))

        while self.comm.has_data():
            print(self.comm.get_data())

    def stop(self):
        self.comm.stop()