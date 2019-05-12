"""this file defines the module for controller_module"""
from client.comm import BaseComm
from common.frame_enum import FrameType


class Module:
    """
    this module listens for an activty led state frame.
    then prints wether the led is supposed to be ON or OFF based on the received frame
    """
    def __init__(self, comm: BaseComm):
        self.comm = comm
        self.comm.listen_for([FrameType.ACTIVITY_LED_STATE])

    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

            if frame.request:
                continue

            if frame["state"]:
                print("The LED is ON")
            else:
                print("The LED is OFF")

    def stop(self):
        self.comm.stop()
