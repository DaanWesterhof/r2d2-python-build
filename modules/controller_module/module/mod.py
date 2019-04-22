from client.comm import Comm
from common.frame_enum import FrameType
from common.frames import FrameActivityLedState


class Module:
    def __init__(self):
        self.comm = Comm()
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

    def stop(self):
        self.comm.stop()
