"""this module provides a dummy Comm class for testing"""
import client.comm

class MockComm(client.comm.BaseComm):
    """dummy Comm class. for testing"""

    def __init__(self, frames=..., *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = frames if frames is not ... else []

    def accepts_frame(self, frame_type):
        return super().accepts_frame(frame_type)

    def get_data(self):
        return super().get_data()

    def has_data(self):
        return super().has_data()

    def listen_for(self, comm_listen_for):
        return super().listen_for(comm_listen_for)

    def request(self, frame_type, prio=client.comm.Priority.NORMAL):
        return super().request(frame_type, prio=prio)

    def send(self, frame, prio=client.comm.Priority.NORMAL):
        return super().send(frame, prio=prio)

    def stop():
        pass
