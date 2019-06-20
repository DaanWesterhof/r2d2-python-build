#! python

"""template module"""

#pylint: disable=unused-import
#pylint: disable=useless-super-delegation

from client.comm import BaseComm
from common.frame_enum import FrameType
from common.base_module import BaseModule


class Module(BaseModule):
    """template module"""
    def __init__(self, comm: BaseComm):
        super(Module, self).__init__(comm)
        # self.comm.listen_for([FrameType.BUTTON_STATE])

    def process(self):
        # self.comm.send(FrameType.BUTTON_STATE, (1,2,3))

        while self.comm.has_data():
            print(self.comm.get_data())
