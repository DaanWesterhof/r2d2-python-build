"""this file defines the module for controller_module"""

from client.comm import BaseComm
from common.frame_enum import FrameType
from common.frames import FrameActivityLedState
from common.base_module import BaseModule

class Module(BaseModule):
    "this module requests a button state and forwards the result as a ActivityLedState"
    def __init__(self, comm: BaseComm):
        super(Module, self).__init__(comm)
        self.comm.listen_for([FrameType.BUTTON_STATE])

    def process(self):
        # Request the button state from the button module
        self.comm.request(FrameType.BUTTON_STATE)

        while self.comm.has_data():
            # Get the frame from the comm module
            frame = self.comm.get_data()

            # Extract the data out of the frame,
            # the result will be a tuple
            data = frame.get_data()

            # We only process answers
            if frame.request:
                continue

            # Create the frame that will be send
            # to the led module
            state = FrameActivityLedState()

            # Set the data.
            state.set_data(data[0])

            # Send it off!
            self.comm.send(state)
