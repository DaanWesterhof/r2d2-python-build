import zmq
import select
from common.common import Frame


class Connection:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)

    def connect(self):
        self.socket.connect('tcp://127.0.0.1:5555')

    def send_object(self, obj):
        self.socket.send_pyobj(obj)

    def send_string(self, string: str):
        self.socket.send_string(string)

    def data_ready(self):
        rs, ws, es = select.select([self.socket], [], [], 0.1)
        return len(rs) > 0
