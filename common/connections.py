import zmq
import select
from .common import Frame, FrameType
from time import sleep
import random


class BaseConn:
    BIND_ADDRESS = 'tcp://127.0.0.1:5555'

    def __init__(self):
        self.context = zmq.Context()
        self.socket = None

    def connect(self):
        self.socket.connect(BaseConn.BIND_ADDRESS)

    def send(self, obj):
        self.socket.send_pyobj(obj)

    def receive(self):
        return self.socket.recv()


class TxConn(BaseConn):
    def __init__(self):
        super().__init__()
        self.socket = self.context.socket(zmq.REP)


class RxConn(BaseConn):
    def __init__(self):
        super().__init__()
        self.socket = self.context.socket(zmq.REQ)

    def has_data(self):
        rs, ws, es = select.select([self.socket], [], [], 0.1)
        return len(rs) > 0
