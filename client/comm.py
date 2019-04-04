from enum import Enum
from common.common import Frame, FrameType
from client import Connection


class Priority(Enum):
    HIGH = 0
    NORMAL = 1
    LOW = 2
    DATA_STREAM = 3


class Comm:
    def __init__(self):
        self.rx_buffer = []
        self.listen_for = []
        self.accepts_all = False
        self.conn = Connection()

    def listen_for(self, listen_for: list):
        self.listen_for = listen_for

        if FrameType.ALL in listen_for:
            self.accepts_all = True

    def accept_frame(self, frame: Frame):
        self.rx_buffer.append(frame)

    def accepts_frame(self, type: FrameType):
        if self.accepts_all:
            return True
        return type in self.listen_for

    def request(self, type, prio: Priority = Priority.NORMAL):
        pass

    def send(self, type, data, prio: Priority = Priority.NORMAL):
        pass

    def has_data(self):
        return len(self.rx_buffer) > 0

    def get_data(self):
        self.rx_buffer.pop(0)
